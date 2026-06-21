| Trường | Ý nghĩa | Ví dụ trong dữ liệu |
| --- | --- | --- |
| **e** | Loại sự kiện (event type) | ``"24hrTicker"`` |
| **E** | Thời gian sự kiện (event time, tính bằng ms từ epoch) | ``1782047329015`` |
| **s** | Ký hiệu (symbol) | ``"ETHUSDT"`` |
| **p** | Thay đổi giá tuyệt đối trong 24h | ``-0.63000000`` |
| **P** | Tỷ lệ phần trăm thay đổi giá trong 24h | ``-0.036`` (≈ -0.036%) |
| **w** | Giá trung bình có trọng số trong 24h | ``1732.35413132`` |
| **x** | Giá mở cửa (open price) | ``1726.87000000`` |
| **c** | Giá cuối cùng (last price) | ``1726.24000000`` |
| **Q** | Khối lượng giao dịch cuối cùng (last quantity) | ``0.02610000`` |
| **b** | Giá bid tốt nhất hiện tại | ``1726.23000000`` |
| **B** | Khối lượng bid tốt nhất | ``13.92520000`` |
| **a** | Giá ask tốt nhất hiện tại | ``1726.24000000`` |
| **A** | Khối lượng ask tốt nhất | ``19.73300000`` |
| **o** | Giá mở cửa (open price) trong 24h | ``1726.87000000`` |
| **h** | Giá cao nhất trong 24h | ``1749.55000000`` |
| **l** | Giá thấp nhất trong 24h | ``1708.11000000`` |
| **v** | Khối lượng giao dịch (base asset volume) trong 24h | ``159049.08240000`` |
| **q** | Khối lượng giao dịch quy đổi sang USDT (quote asset volume) | ``275529334.97759700`` |
| **O** | Thời gian mở thống kê (statistics open time, ms) | ``1781960929014`` |
| **C** | Thời gian đóng thống kê (statistics close time, ms) | ``1782047329014`` |
| **F** | ID giao dịch đầu tiên trong 24h | ``4147890492`` |
| **L** | ID giao dịch cuối cùng trong 24h | ``4149667633`` |
| **n** | Tổng số giao dịch trong 24h | ``1777142`` |


Nếu bạn muốn giá hiện tại (last price) thì trường cần lấy là:
c (last price) → đây chính là giá khớp lệnh cuối cùng trong thời điểm gửi dữ liệu.