from PIL import Image
import numpy as np
import os


class ImageSteganography:
    def __init__(self):
        self.delimiter = "$$$END$$$"  # Penanda akhir pesan
    
    def text_to_binary(self, text):
        #Konversi text ke representasi binary
        return ''.join(format(ord(char), '08b') for char in text)
    
    def binary_to_text(self, binary):
        #Konversi binary ke text
        text = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                text += chr(int(byte, 2))
        return text
    
    def calculate_capacity(self, image_path):
        try:
            img = Image.open(image_path)
            width, height = img.size
            total_pixels = width * height * 3  # RGB
            
            # 1 karakter = 8 bits, minus delimiter
            max_chars = (total_pixels // 8) - len(self.delimiter) - 1
            
            return max_chars, width, height, total_pixels
        except Exception as e:
            return 0, 0, 0, 0
    
    def embed_message(self, image_path, message, output_path):
        try:
            # Load dan convert image ke RGB
            img = Image.open(image_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            img_array = np.array(img)
            
            # Tambahkan delimiter
            full_message = message + self.delimiter
            binary_message = self.text_to_binary(full_message)
            
            # Validasi kapasitas
            max_bits = img_array.size
            if len(binary_message) > max_bits:
                return False, f"Pesan terlalu panjang! Maksimal ~{max_bits // 8} karakter."
            
            # Flatten array untuk manipulasi LSB
            flat_img = img_array.flatten()
            
            # Embed message ke LSB
            for i, bit in enumerate(binary_message):
                flat_img[i] = (flat_img[i] & 0xFE) | int(bit)
            
            # Reshape dan save
            stego_array = flat_img.reshape(img_array.shape)
            stego_img = Image.fromarray(stego_array.astype('uint8'), mode='RGB')
            stego_img.save(output_path, 'PNG')

            return True, f"Berhasil! Pesan ({len(message)} karakter) disembunyikan dalam gambar."
        
        except FileNotFoundError:
            return False, "File gambar tidak ditemukan!"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def extract_message(self, stego_image_path):
        try:
            # Load stego image
            img = Image.open(stego_image_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            img_array = np.array(img)
            flat_img = img_array.flatten()
            
            # Ekstrak bit dari LSB
            binary_message = ''
            for pixel_value in flat_img:
                binary_message += str(pixel_value & 1)
            
            # Convert ke text
            full_text = self.binary_to_text(binary_message)
            
            # Cari delimiter
            if self.delimiter in full_text:
                message = full_text.split(self.delimiter)[0]
                return True, message
            else:
                return False, "Tidak ada pesan tersembunyi ditemukan dalam gambar ini."
        
        except FileNotFoundError:
            return False, "File gambar tidak ditemukan!"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def compare_images(self, original_path, stego_path):
        try:
            orig_img = Image.open(original_path)
            stego_img = Image.open(stego_path)

            orig_array = np.array(orig_img)
            stego_array = np.array(stego_img)
            
            # Hitung perbedaan
            diff = np.abs(orig_array.astype(int) - stego_array.astype(int))
            
            return {
                'max_difference': int(np.max(diff)),
                'avg_difference': float(np.mean(diff)),
                'changed_pixels': int(np.sum(diff > 0)),
                'total_pixels': orig_array.size,
                'percentage_changed': (np.sum(diff > 0) / orig_array.size) * 100
            }
        except Exception as e:
            return None

