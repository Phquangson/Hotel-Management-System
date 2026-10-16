"""file_handler.py - Lưu / đọc dữ liệu JSON."""
import json
import os

from models import Phong, PhongThuong, PhongVIP, KhachHang, PhieuThue, TRONG, DA_THUE

FILE_DATA = "khachsan_data.json"


def save_data(danh_sach_phong, danh_sach_phieu, lich_su=None, filename=FILE_DATA):
    """Ghi phòng, phiếu thuê (và lịch sử doanh thu) ra file JSON."""
    data = {
        "phong": [p.to_dict() for p in danh_sach_phong],
        "phieu_thue": [pt.to_dict() for pt in danh_sach_phieu],
        "lich_su": lich_su or [],
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def _tao_phong(d):
    if d["loai"] == "VIP":
        p = PhongVIP(d["ma_phong"], d["ten_phong"], d["gia_co_ban"],
                     d.get("phi_don_dep", 0), d.get("phi_minibar", 0),
                     d.get("trang_thai", TRONG))
    else:
        p = PhongThuong(d["ma_phong"], d["ten_phong"], d["gia_co_ban"],
                        d.get("trang_thai", TRONG))
    return p


def load_data(filename=FILE_DATA):
    """Đọc dữ liệu. Trả về (danh_sach_phong, danh_sach_phieu, lich_su).
    Nếu file chưa tồn tại hoặc hỏng -> trả về dữ liệu rỗng, không văng lỗi."""
    if not os.path.exists(filename):
        return [], [], []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        phongs = [_tao_phong(d) for d in data.get("phong", [])]
        tra_cuu = {p.ma_phong: p for p in phongs}

        phieus = []
        for d in data.get("phieu_thue", []):
            phong = tra_cuu.get(d["ma_phong"])
            if phong is None:
                continue  # bỏ qua phiếu trỏ tới phòng không còn tồn tại
            k = d["khach_hang"]
            khach = KhachHang(k["ma_khach"], k["ten"], k["cccd"])
            phieus.append(PhieuThue(khach, phong, d["so_ngay"]))

        return phongs, phieus, data.get("lich_su", [])
    except (json.JSONDecodeError, KeyError, TypeError, OSError) as e:
        print(f"[Cảnh báo] Không đọc được file dữ liệu ({e}). Khởi động với dữ liệu trống.")
        return [], [], []