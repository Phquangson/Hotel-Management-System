"""models.py - Các lớp đối tượng của hệ thống quản lý khách sạn."""

TRONG = "Trống"
DA_THUE = "Đã thuê"


class Phong:
    """Lớp cơ sở cho mọi loại phòng."""

    def __init__(self, ma_phong, ten_phong, gia_co_ban, trang_thai=TRONG):
        self.ma_phong = ma_phong
        self.ten_phong = ten_phong
        self.gia_co_ban = gia_co_ban
        self.__trang_thai = trang_thai  # private: chỉ đổi qua phương thức

    # --- Đóng gói trạng thái ---
    @property
    def trang_thai(self):
        return self.__trang_thai

    def la_trong(self):
        return self.__trang_thai == TRONG

    def thue_phong(self):
        if not self.la_trong():
            raise ValueError(f"Phòng {self.ma_phong} đã có người thuê.")
        self.__trang_thai = DA_THUE

    def tra_phong(self):
        self.__trang_thai = TRONG

    # --- Đa hình: lớp con sẽ ghi đè ---
    def tinh_tien(self, so_ngay):
        raise NotImplementedError("Lớp con phải cài đặt tinh_tien()")

    def loai_phong(self):
        return "Phong"

    def to_dict(self):
        return {
            "loai": self.loai_phong(),
            "ma_phong": self.ma_phong,
            "ten_phong": self.ten_phong,
            "gia_co_ban": self.gia_co_ban,
            "trang_thai": self.__trang_thai,
        }

    def __str__(self):
        return (f"{self.ma_phong:<8}{self.ten_phong:<20}{self.loai_phong():<12}"
                f"{self.gia_co_ban:>12,.0f}  {self.trang_thai}")


class PhongThuong(Phong):
    """Phòng thường: không có phí phụ thu."""

    def tinh_tien(self, so_ngay):
        return self.gia_co_ban * so_ngay

    def loai_phong(self):
        return "Thường"


class PhongVIP(Phong):
    """Phòng VIP: cộng thêm phí dọn dẹp và phí minibar."""

    def __init__(self, ma_phong, ten_phong, gia_co_ban,
                 phi_don_dep=0, phi_minibar=0, trang_thai=TRONG):
        super().__init__(ma_phong, ten_phong, gia_co_ban, trang_thai)
        self.phi_don_dep = phi_don_dep
        self.phi_minibar = phi_minibar

    def tinh_tien(self, so_ngay):
        return self.gia_co_ban * so_ngay + self.phi_don_dep + self.phi_minibar

    def loai_phong(self):
        return "VIP"

    def to_dict(self):
        d = super().to_dict()
        d["phi_don_dep"] = self.phi_don_dep
        d["phi_minibar"] = self.phi_minibar
        return d


class KhachHang:
    def __init__(self, ma_khach, ten, cccd):
        self.ma_khach = ma_khach
        self.ten = ten
        self.cccd = cccd

    def to_dict(self):
        return {"ma_khach": self.ma_khach, "ten": self.ten, "cccd": self.cccd}


class PhieuThue:
    def __init__(self, khach_hang, phong, so_ngay):
        self.khach_hang = khach_hang
        self.phong = phong
        self.so_ngay = so_ngay

    def tong_tien(self):
        return self.phong.tinh_tien(self.so_ngay)  # đa hình

    def to_dict(self):
        return {
            "khach_hang": self.khach_hang.to_dict(),
            "ma_phong": self.phong.ma_phong,
            "so_ngay": self.so_ngay,
        }