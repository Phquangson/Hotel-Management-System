"""services.py - Nghiệp vụ lõi của khách sạn."""
from models import PhongThuong, PhongVIP, KhachHang, PhieuThue
import file_handler


class LoiNghiepVu(Exception):
    """Lỗi nghiệp vụ (phòng không tồn tại, phòng đã thuê, ...)."""


class QuanLyKhachSan:
    def __init__(self):
        self.danh_sach_phong = []
        self.danh_sach_phieu = []   # các phiếu thuê hiện tại
        self.lich_su = []           # lịch sử doanh thu
        self.tai_du_lieu()

    # ---------- Lưu trữ ----------
    def tai_du_lieu(self):
        self.danh_sach_phong, self.danh_sach_phieu, self.lich_su = file_handler.load_data()

    def luu_du_lieu(self):
        file_handler.save_data(self.danh_sach_phong, self.danh_sach_phieu, self.lich_su)

    # ---------- Tiện ích ----------
    def tim_phong(self, ma_phong):
        for p in self.danh_sach_phong:
            if p.ma_phong.lower() == ma_phong.lower():
                return p
        return None

    # ---------- Thêm phòng ----------
    def them_phong(self, phong):
        if self.tim_phong(phong.ma_phong):
            raise LoiNghiepVu(f"Mã phòng '{phong.ma_phong}' đã tồn tại.")
        self.danh_sach_phong.append(phong)

    # ---------- Đặt phòng ----------
    def dat_phong(self, ma_phong, khach, so_ngay):
        if so_ngay <= 0:
            raise LoiNghiepVu("Số ngày thuê phải lớn hơn 0.")
        phong = self.tim_phong(ma_phong)
        if phong is None:
            raise LoiNghiepVu(f"Phòng '{ma_phong}' không tồn tại.")
        if not phong.la_trong():
            raise LoiNghiepVu(f"Phòng '{phong.ma_phong}' đã có người thuê.")
        phong.thue_phong()
        phieu = PhieuThue(khach, phong, so_ngay)
        self.danh_sach_phieu.append(phieu)
        return phieu

    # ---------- Trả phòng ----------
    def tra_phong(self, ma_phong):
        phong = self.tim_phong(ma_phong)
        if phong is None:
            raise LoiNghiepVu(f"Phòng '{ma_phong}' không tồn tại.")
        phieu = next((pt for pt in self.danh_sach_phieu if pt.phong is phong), None)
        if phieu is None:
            raise LoiNghiepVu(f"Phòng '{phong.ma_phong}' hiện đang trống, không có phiếu thuê.")

        tong_tien = phieu.tong_tien()
        phong.tra_phong()
        self.danh_sach_phieu.remove(phieu)
        self.lich_su.append({
            "ma_phong": phong.ma_phong,
            "ten_khach": phieu.khach_hang.ten,
            "so_ngay": phieu.so_ngay,
            "tong_tien": tong_tien,
        })
        return phieu, tong_tien

    # ---------- Báo cáo ----------
    def tong_doanh_thu(self):
        return sum(item["tong_tien"] for item in self.lich_su)

    def so_phong_trong(self):
        return sum(1 for p in self.danh_sach_phong if p.la_trong())