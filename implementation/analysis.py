import cv2
import numpy as np
import os
import glob
from skimage.metrics import structural_similarity as ssim
import pandas as pd

class PVDExperimentAnalysis:
    def __init__(self):
        self.results = []
        self.supported_extensions = ['*.bmp', '*.png', '*.BMP', '*.PNG']
    
    def load_image_safely(self, image_path):
        """Tải hình ảnh một cách an toàn với kiểm tra lỗi"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Không tìm thấy file: {image_path}")
        
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Không thể đọc file hình ảnh: {image_path}")
        
        return image
    
    def get_image_files(self, directory):
        """Lấy danh sách tất cả file ảnh trong thư mục"""
        image_files = []
        for extension in self.supported_extensions:
            pattern = os.path.join(directory, extension)
            image_files.extend(glob.glob(pattern))
        return sorted(image_files)
    
    def get_base_filename(self, filepath):
        """Lấy tên file không có phần mở rộng"""
        return os.path.splitext(os.path.basename(filepath))[0]
    
    def find_image_pairs(self, original_dir, stego_dir):
        """Tìm các cặp ảnh gốc và stego tương ứng"""
        original_files = self.get_image_files(original_dir)
        stego_files = self.get_image_files(stego_dir)
        
        pairs = []
        found_pairs = set()  # Thêm set để tránh trùng lặp cặp
        
        print(f"Tìm thấy {len(original_files)} ảnh gốc trong {original_dir}")
        print(f"Tìm thấy {len(stego_files)} ảnh stego trong {stego_dir}")
        print(f"Danh sách ảnh gốc: {[os.path.basename(f) for f in original_files]}")
        print(f"Danh sách ảnh stego: {[os.path.basename(f) for f in stego_files]}")
        print()
        
        for original_file in original_files:
            original_base = self.get_base_filename(original_file)
            
            # Tìm file stego tương ứng (tên gốc + "_stego")
            stego_name = original_base + "_stego"
            
            matching_stego = None
            for stego_file in stego_files:
                stego_base = self.get_base_filename(stego_file)
                if stego_base == stego_name:
                    matching_stego = stego_file
                    break
            
            if matching_stego:
                # Tạo key duy nhất cho cặp này
                pair_key = (original_base, self.get_base_filename(matching_stego))
                
                if pair_key not in found_pairs:
                    pairs.append((original_file, matching_stego, original_base))
                    found_pairs.add(pair_key)
                    print(f"✓ Tìm thấy cặp: {os.path.basename(original_file)} <-> {os.path.basename(matching_stego)}")
                else:
                    print(f"⚠ Bỏ qua cặp trùng lặp: {original_base}")
            else:
                print(f"✗ Không tìm thấy ảnh stego cho: {os.path.basename(original_file)}")
        
        print(f"\nTổng cộng tìm thấy {len(pairs)} cặp ảnh duy nhất để phân tích.")
        return pairs
    
    def calculate_psnr(self, original, compressed):
        """Tính PSNR giữa hai hình ảnh"""
        if original is None or compressed is None:
            raise ValueError("Hình ảnh đầu vào không hợp lệ (None)")
        
        # Đảm bảo cùng kích thước
        if original.shape != compressed.shape:
            raise ValueError("Kích thước hai hình ảnh không khớp")
        
        mse = np.mean((original.astype(float) - compressed.astype(float)) ** 2)
        if mse == 0:
            return float('inf')  # Hình ảnh giống hệt nhau
        
        max_pixel = 255.0
        psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
        return psnr
    
    def calculate_mse(self, original, compressed):
        """Tính Mean Square Error"""
        if original is None or compressed is None:
            raise ValueError("Hình ảnh đầu vào không hợp lệ (None)")
        
        return np.mean((original.astype(float) - compressed.astype(float)) ** 2)
    
    def calculate_ssim(self, original, compressed):
        """Tính Structural Similarity Index"""
        if original is None or compressed is None:
            raise ValueError("Hình ảnh đầu vào không hợp lệ (None)")
        
        # Chuyển sang grayscale nếu là ảnh màu
        if len(original.shape) == 3:
            original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            compressed_gray = cv2.cvtColor(compressed, cv2.COLOR_BGR2GRAY)
        else:
            original_gray = original
            compressed_gray = compressed
        
        return ssim(original_gray, compressed_gray)
    
    def calculate_embedding_capacity(self, image_shape):
        """Tính dung lượng nhúng tối đa cho PVD"""
        height, width = image_shape[:2]
        # PVD có thể nhúng 3-7 bits mỗi cặp pixel tùy vào range
        max_pairs = (height * width) // 2
        # Trung bình 5 bits mỗi cặp (ước tính)
        return max_pairs * 5
    
    def estimate_payload_size(self, original_path, stego_path):
        """Ước tính kích thước payload dựa trên sự khác biệt giữa 2 file"""
        try:
            original_size = os.path.getsize(original_path)
            stego_size = os.path.getsize(stego_path)
            # Ước tính payload (có thể không chính xác 100%)
            size_diff = abs(stego_size - original_size)
            # Nếu không có sự khác biệt đáng kể, ước tính khoảng 1KB
            return max(size_diff, 1024)  # ít nhất 1KB
        except:
            return 1024  # mặc định 1KB
    
    def analyze_image_pair(self, original_path, stego_path, image_name=""):
        """Phân tích một cặp hình ảnh gốc và stego"""
        try:
            # Tải hình ảnh
            original = self.load_image_safely(original_path)
            stego = self.load_image_safely(stego_path)
            
            print(f"\n--- Phân tích: {image_name} ---")
            print(f"Kích thước hình gốc: {original.shape}")
            print(f"Kích thước hình stego: {stego.shape}")
            
            # Tính các thông số
            psnr = self.calculate_psnr(original, stego)
            mse = self.calculate_mse(original, stego)
            ssim_score = self.calculate_ssim(original, stego)
            
            # In kết quả
            print(f"PSNR: {psnr:.2f} dB")
            print(f"MSE: {mse:.2f}")
            print(f"SSIM: {ssim_score:.4f}")
            
            # Lưu kết quả chỉ với các cột cần thiết
            result = {
                'image_name': image_name,
                'image_size': f"{original.shape[1]}x{original.shape[0]}",
                'psnr': psnr,
                'mse': mse,
                'ssim': ssim_score
            }
            self.results.append(result)
            
            return result
            
        except Exception as e:
            print(f"Lỗi khi phân tích {original_path}: {str(e)}")
            return None

    def generate_report_table(self):
        """Tạo bảng báo cáo kết quả"""
        if not self.results:
            print("Chưa có dữ liệu để tạo báo cáo")
            return
        
        # Loại bỏ các kết quả trùng lặp dựa trên tên ảnh
        unique_results = []
        seen_names = set()
        
        for result in self.results:
            if result['image_name'] not in seen_names:
                unique_results.append(result)
                seen_names.add(result['image_name'])
        
        df = pd.DataFrame(unique_results)
        print("\n" + "="*60)
        print("                BẢNG KẾT QUẢ THỰC NGHIỆM PVD")
        print("="*60)
        
        # Format bảng đẹp
        print(f"{'Hình ảnh':<15} {'Kích thước':<12} {'PSNR':<8} {'MSE':<8} {'SSIM':<8}")
        print(f"{'(tên)':<15} {'(WxH)':<12} {'(dB)':<8} {'()':<8} {'()':<8}")
        print("-" * 60)
        
        for _, row in df.iterrows():
            print(f"{row['image_name']:<15} {row['image_size']:<12} "
                  f"{row['psnr']:<8.2f} {row['mse']:<8.2f} {row['ssim']:<8.4f}")
        
        print("-" * 60)
        print(f"Trung bình:     {'':>14} "
              f"{df['psnr'].mean():<8.2f} {df['mse'].mean():<8.2f} {df['ssim'].mean():<8.4f}")
        print("="*60)
        print(f"Số lượng ảnh phân tích: {len(unique_results)}")
        
        return df
    
    def save_results_to_excel(self, filename="pvd_experiment_results.xlsx"):
        """Lưu kết quả ra file Excel"""
        if not self.results:
            print("Chưa có dữ liệu để lưu")
            return
        
        df = pd.DataFrame(self.results)
        
        # Chỉ thêm dòng trung bình
        stats = {
            'image_name': ['TRUNG BÌNH'],
            'image_size': [''],
            'psnr': [df['psnr'].mean()],
            'mse': [df['mse'].mean()],
            'ssim': [df['ssim'].mean()]
        }
        
        stats_df = pd.DataFrame(stats)
        final_df = pd.concat([df, stats_df], ignore_index=True)
        
        final_df.to_excel(filename, index=False)
        print(f"Đã lưu kết quả vào file: {filename}")

def main():
    analyzer = PVDExperimentAnalysis()
    
    try:
        # Đường dẫn thư mục
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        original_dir = os.path.join(BASE_DIR, "images", "original")
        stego_dir = os.path.join(BASE_DIR, "images", "stego")
        
        # Kiểm tra thư mục có tồn tại không
        if not os.path.exists(original_dir):
            raise FileNotFoundError(f"Thư mục không tồn tại: {original_dir}")
        if not os.path.exists(stego_dir):
            raise FileNotFoundError(f"Thư mục không tồn tại: {stego_dir}")
        
        print("PHẦN MỀM PHÂN TÍCH THỰC NGHIỆM PVD")
        print("="*50)
        print(f"Thư mục ảnh gốc: {original_dir}")
        print(f"Thư mục ảnh stego: {stego_dir}")
        print(f"Định dạng hỗ trợ: BMP, PNG")
        print()
        
        # Tìm các cặp ảnh
        image_pairs = analyzer.find_image_pairs(original_dir, stego_dir)
        
        if not image_pairs:
            print("Không tìm thấy cặp ảnh nào để phân tích!")
            print("\nLưu ý: Ảnh stego phải có tên theo định dạng: [tên_ảnh_gốc]_stego.[định_dạng]")
            print("Ví dụ: lena.jpg -> lena_stego.png")
            return
        
        print(f"\nBắt đầu phân tích {len(image_pairs)} cặp ảnh...")
        
        # Phân tích từng cặp
        success_count = 0
        for original_path, stego_path, image_name in image_pairs:
            result = analyzer.analyze_image_pair(original_path, stego_path, image_name)
            if result:
                success_count += 1
        
        print(f"\nĐã phân tích thành công {success_count}/{len(image_pairs)} cặp ảnh.")
        
        # Tạo báo cáo
        if analyzer.results:
            analyzer.generate_report_table()
            
            # Lưu Excel
            output_file = os.path.join(BASE_DIR, "pvd_experiment_results.xlsx")
            analyzer.save_results_to_excel(output_file)
            
            print(f"\n✓ Hoàn thành! Kết quả đã được lưu vào {output_file}")
        
    except Exception as e:
        print(f"Lỗi trong quá trình thực nghiệm: {str(e)}")
        print("\nHướng dẫn khắc phục:")
        print("1. Tạo thư mục 'images/original/' và 'images/stego/' nếu chưa có")
        print("2. Đặt hình ảnh gốc vào thư mục 'images/original/'")
        print("3. Đặt hình ảnh stego vào thư mục 'images/stego/' với tên: [tên_gốc]_stego.[định_dạng]")
        print("4. Đảm bảo định dạng file là BMP hoặc PNG")
        print("\nVí dụ cấu trúc thư mục:")
        print("images/")
        print("├── original/")
        print("│   ├── lena.png")
        print("│   └── baboon.bmp")
        print("└── stego/")
        print("    ├── lena_stego.png")
        print("    └── baboon_stego.png")

if __name__ == "__main__":
    main()