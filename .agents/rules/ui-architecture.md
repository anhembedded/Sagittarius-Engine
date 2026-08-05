# UI Architecture Guidelines (PySide + Clean Architecture)

Để xây dựng một ứng dụng PySide có nhiều màn hình (Multi-screen) và quản lý giao diện theo mô hình Thẻ (Card UI Pattern) tuân thủ tuyệt đối Clean Architecture, bài toán được chia thành 3 tầng rõ rệt:
1. **Component (Các Thẻ Card)**: Những mảnh ghép nhỏ, độc lập, có thể tái sử dụng ở bất kỳ đâu.
2. **Screen/View (Màn hình)**: Nơi lắp ghép các thẻ Card lại với nhau (như chơi Lego).
3. **Router (Cửa sổ chính)**: Khung điều hướng chứa menu bên trái và khu vực chuyển màn hình bên phải.

## 1. Cấu trúc thư mục tiêu chuẩn
Tổ chức thư mục UI như sau để dự án không bị rối:
```text
src/presentation/ui/
├── main_window.py               # Cửa sổ gốc, chứa Menu Sidebar & QStackedWidget (Router)
├── components/                  # Nơi chứa các "Thẻ Card" dùng chung
│   ├── __init__.py
│   └── chart_card.py            # Widget Thẻ biểu đồ + nút bấm
└── screens/                     # Nơi chứa các màn hình cụ thể
    ├── dashboard/
    │   ├── dashboard_view.py    # Giao diện màn hình Dashboard (chứa nhiều Card)
    │   └── dashboard_presenter.py # Não bộ xử lý logic của Dashboard
    └── backtest/
        ├── backtest_view.py
        └── backtest_presenter.py
```

## 2. Tạo "Thẻ" tái sử dụng (Card Component)
Một Card phải "ngu" (Dumb Component) - tức là nó không được chứa bất kỳ logic gọi Database hay Use Case nào. Khi người dùng bấm nút trên Card, nó chỉ phát ra một tín hiệu (Signal).

**File:** `src/presentation/ui/components/chart_card.py`
```python
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import Signal
import pyqtgraph as pg

class ChartCard(QFrame):
    # 1. Định nghĩa các Tín hiệu (Signals) để giao tiếp ra bên ngoài
    run_requested = Signal(str)  # Truyền ra chuỗi (ví dụ: tên symbol)
    stop_requested = Signal()

    def __init__(self, title: str, symbol_name: str, parent=None):
        super().__init__(parent)
        self.symbol_name = symbol_name
        
        # Style cho Card: Bo góc, nền tối, viền mờ
        self.setObjectName("Card")
        self.setStyleSheet("""
            #Card {
                background-color: #2b2b2b;
                border: 1px solid #3d3d3d;
                border-radius: 10px;
            }
        """)

        # Layout chính của Thẻ (Dọc)
        main_layout = QVBoxLayout(self)

        # --- Header ---
        self.lbl_title = QLabel(title)
        self.lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff; padding: 5px;")
        main_layout.addWidget(self.lbl_title)

        # --- Body: Biểu đồ (Dùng pyqtgraph) ---
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setMinimumHeight(250)
        main_layout.addWidget(self.plot_widget)

        # --- Footer: Nút bấm (Ngang) ---
        footer_layout = QHBoxLayout()
        self.btn_run = QPushButton("▶ Run")
        self.btn_stop = QPushButton("■ Stop")
        
        # Gắn sự kiện click vào Signal
        self.btn_run.clicked.connect(lambda: self.run_requested.emit(self.symbol_name))
        self.btn_stop.clicked.connect(self.stop_requested.emit)

        footer_layout.addWidget(self.btn_run)
        footer_layout.addWidget(self.btn_stop)
        footer_layout.addStretch() # Đẩy các nút sang trái
        
        main_layout.addLayout(footer_layout)
        
    def update_chart(self, data):
        """Hàm này để View gọi vào khi có dữ liệu mới"""
        # Cập nhật pyqtgraph ở đây...
        pass
```

## 3. Tạo Màn hình (Screen/View)
Màn hình chỉ làm nhiệm vụ lấy các Thẻ (Card) ghép lại với nhau theo bố cục (Grid, Box).

**File:** `src/presentation/ui/screens/dashboard/dashboard_view.py`
```python
from PySide6.QtWidgets import QWidget, QGridLayout
from src.presentation.ui.components.chart_card import ChartCard

class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Dùng Lưới (Grid) để xếp các Card
        layout = QGridLayout(self)
        
        # Tạo 2 thẻ Card cho 2 đồng coin khác nhau
        self.card_btc = ChartCard(title="Bitcoin Live", symbol_name="BTCUSDT")
        self.card_eth = ChartCard(title="Ethereum Live", symbol_name="ETHUSDT")
        
        # Ép vào lưới: Hàng, Cột
        layout.addWidget(self.card_btc, 0, 0) # Hàng 0, Cột 0
        layout.addWidget(self.card_eth, 0, 1) # Hàng 0, Cột 1
```

## 4. Não bộ của Màn hình (Presenter)
Đây là nơi lắng nghe tín hiệu từ các Card trong View, và ra lệnh cho hệ thống (qua sagittarius_engine).

**File:** `src/presentation/ui/screens/dashboard/dashboard_presenter.py`
```python
# Giả sử bạn có class App của sagittarius_engine
# from application.use_cases.stream.command import StartLiveStreamCommand

class DashboardPresenter:
    def __init__(self, view: DashboardView, app):
        self.view = view
        self.app = app
        
        self._connect_signals()

    def _connect_signals(self):
        # Nối tín hiệu từ Card BTC vào hàm xử lý
        self.view.card_btc.run_requested.connect(self.on_start_stream)
        self.view.card_eth.run_requested.connect(self.on_start_stream)
        
    def on_start_stream(self, symbol: str):
        print(f"Presenter nhận lệnh chạy stream cho: {symbol}")
        # Tại đây bạn tạo Command và đưa cho engine chạy
        # cmd = StartLiveStreamCommand(symbols=[symbol])
        # self.app.dispatch(StartLiveStreamCommand, cmd)
```

## 5. Trạm trung chuyển (Cửa sổ chính - Router)
Để có Menu bên trái (Sidebar) bấm chuyển qua lại giữa các màn hình, ta dùng QStackedWidget.

**File:** `src/presentation/ui/main_window.py`
```python
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget
from src.presentation.ui.screens.dashboard.dashboard_view import DashboardView
from src.presentation.ui.screens.dashboard.dashboard_presenter import DashboardPresenter

class MainWindow(QMainWindow):
    def __init__(self, app_instance):
        super().__init__()
        self.setWindowTitle("Binance Trading Bot")
        self.resize(1200, 800)
        
        # Widget gốc chứa toàn bộ
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # --- 1. Tạo Sidebar (Menu bên trái) ---
        sidebar_layout = QVBoxLayout()
        self.btn_nav_dashboard = QPushButton("Dashboard")
        self.btn_nav_backtest = QPushButton("Backtest")
        
        sidebar_layout.addWidget(self.btn_nav_dashboard)
        sidebar_layout.addWidget(self.btn_nav_backtest)
        sidebar_layout.addStretch()
        
        # --- 2. Tạo Stacked Widget (Nơi chứa các màn hình) ---
        self.stacked_widget = QStackedWidget()
        
        # Khởi tạo Màn hình Dashboard & Presenter của nó
        self.dashboard_view = DashboardView()
        self.dashboard_presenter = DashboardPresenter(self.dashboard_view, app_instance)
        
        # Khởi tạo Màn hình Backtest (Giả sử bạn đã code BacktestView)
        self.backtest_view = QWidget() # Tạm placeholder
        
        # Nhét các màn hình vào Stack
        self.stacked_widget.addWidget(self.dashboard_view) # Index 0
        self.stacked_widget.addWidget(self.backtest_view)  # Index 1
        
        # --- 3. Ghép Sidebar và Stacked Widget vào layout chính ---
        main_layout.addLayout(sidebar_layout, stretch=1)
        main_layout.addWidget(self.stacked_widget, stretch=5)
        
        # --- 4. Gắn sự kiện chuyển trang ---
        self.btn_nav_dashboard.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_nav_backtest.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
```

## Tổng kết Luồng dữ liệu (Data Flow)
Kiến trúc này hoạt động như một dây chuyền cực kỳ chặt chẽ:
1. Bạn bấm nút "▶ Run" trên Thẻ BTC.
2. `ChartCard` không tự gọi Database, nó chỉ hét lên: `run_requested.emit("BTCUSDT")`.
3. `DashboardPresenter` (đang vểnh tai nghe ngóng) bắt được tiếng hét này $\rightarrow$ Nó biết có người muốn chạy luồng BTC.
4. `DashboardPresenter` gói yêu cầu thành `StartLiveStreamCommand` và đẩy vào cho `app.dispatch()`.
5. Khi có data mới chạy ngầm từ Binance trả về qua Event Bus, `DashboardPresenter` bắt lấy, ném lại vào hàm `card_btc.update_chart(data)` để biểu đồ nhảy số.

Cách làm này đảm bảo ứng dụng có to lên hàng chục màn hình, hàng trăm thẻ Card thì code vẫn gọn gàng, tách bạch và chuẩn 100% Clean Architecture!
