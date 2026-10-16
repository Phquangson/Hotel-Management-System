"""main.py - Giao diện dòng lệnh (CLI) quản lý khách sạn."""
from models import PhongThuong, PhongVIP, KhachHang
from services import QuanLyKhachSan, LoiNghiepVu


def nhap_so_nguyen(thong_bao):
    while True:
        try:
            return int(input(thong_bao))
        except ValueError:
            print("  ! Vui lòng nhập một số nguyên hợp lệ.")


def nhap_so_thuc(thong_bao):
    while True:
        try:
            return float(input(thong_bao))
        except ValueError:
            print("  ! Vui lòng nhập một số hợp lệ.")


def nhap_chuoi(thong_bao):
    while True:
        s = input(thong_bao).strip()
        if s:
            return s
        print("  ! Không được để trống.")


def hien_thi_phong(ql):
    if not ql.danh_sach_phong:
        print("Chưa có phòng nào trong hệ thống.")
        return
    print(f"{'Mã':<8}{'Tên phòng':<20}{'Loại':<12}{'Giá cơ bản':>12}  Trạng thái")
    print("-" * 66)
    for p in ql.danh_sach_phong:
        print(p)


def them_phong(ql):
    loai = input("Loại phòng (1: Thường, 2: VIP): ").strip()
    if loai not in ("1", "2"):
        print("  ! Loại phòng không hợp lệ.")
        return
    ma = nhap_chuoi("Mã phòng: ")
    ten = nhap_chuoi("Tên phòng: ")
    gia = nhap_so_thuc("Giá cơ bản/ngày: ")
    if gia < 0:
        print("  ! Giá không được âm.")
        return
    if loai == "1":
        phong = PhongThuong(ma, ten, gia)
    else:
        don_dep = nhap_so_thuc("Phí dịch vụ dọn dẹp: ")
        minibar = nhap_so_thuc("Phí minibar: ")
        if don_dep < 0 or minibar < 0:
            print("  ! Phí không được âm.")
            return
        phong = PhongVIP(ma, ten, gia, don_dep, minibar)
    ql.them_phong(phong)
    print("Đã thêm phòng thành công.")


def dat_phong(ql):
    ma_phong = nhap_chuoi("Mã phòng muốn đặt: ")
    ma_khach = nhap_chuoi("Mã khách: ")
    ten = nhap_chuoi("Tên khách: ")
    cccd = nhap_chuoi("Số CCCD/CMND: ")
    so_ngay = nhap_so_nguyen("Số ngày thuê: ")
    phieu = ql.dat_phong(ma_phong, KhachHang(ma_khach, ten, cccd), so_ngay)
    print(f"Đặt phòng thành công! Khách {ten} thuê phòng {phieu.phong.ma_phong} "
          f"trong {so_ngay} ngày.")


def tra_phong(ql):
    ma_phong = nhap_chuoi("Mã phòng cần trả: ")
    phieu, tong = ql.tra_phong(ma_phong)
    print(f"Khách: {phieu.khach_hang.ten} | Phòng: {phieu.phong.ma_phong} "
          f"({phieu.phong.loai_phong()}) | {phieu.so_ngay} ngày")
    print(f"TỔNG TIỀN PHẢI TRẢ: {tong:,.0f} VNĐ")


def bao_cao(ql):
    print("===== BÁO CÁO DOANH THU =====")
    print(f"Tổng doanh thu     : {ql.tong_doanh_thu():,.0f} VNĐ")
    print(f"Số lượt trả phòng  : {len(ql.lich_su)}")
    print(f"Số phòng đang trống: {ql.so_phong_trong()}/{len(ql.danh_sach_phong)}")


def main():
    ql = QuanLyKhachSan()
    chuc_nang = {
        "1": hien_thi_phong,
        "2": them_phong,
        "3": dat_phong,
        "4": tra_phong,
        "5": bao_cao,
    }
    while True:
        print("\n===== QUẢN LÝ KHÁCH SẠN =====")
        print("1. Hiển thị danh sách phòng")
        print("2. Thêm phòng mới")
        print("3. Đặt phòng")
        print("4. Trả phòng & Thanh toán")
        print("5. Xem báo cáo doanh thu")
        print("6. Thoát & Lưu dữ liệu")
        lua_chon = input("Chọn chức năng: ").strip()

        if lua_chon == "6":
            try:
                ql.luu_du_lieu()
                print("Đã lưu dữ liệu. Tạm biệt!")
            except OSError as e:
                print(f"Lỗi khi lưu file: {e}")
            break

        ham = chuc_nang.get(lua_chon)
        if ham is None:
            print("  ! Lựa chọn không hợp lệ, vui lòng chọn 1-6.")
            continue
        try:
            ham(ql)
        except LoiNghiepVu as e:
            print(f"  ! Lỗi: {e}")
        except ValueError as e:
            print(f"  ! Dữ liệu không hợp lệ: {e}")
        except (KeyboardInterrupt, EOFError):
            print("\n  ! Đã hủy thao tác.")


if __name__ == "__main__":
    main()