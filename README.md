# 📊 Finance Tracker Pro

A professional, full-stack web application for personal finance management, built using **Python** and the **Reflex** framework. This project features dynamic data visualizations, smart keyboard navigation, and a polished user interface.

## 🚀 Features

- **Dynamic Financial Dashboard**: Real-time tracking of Income, Expenses, and Balance.
- **Visual Analytics**: Interactive Pie charts for income/expense split and Bar charts for spending by category using `rx.recharts`.
- **Professional UX**: 
  - Smart **Enter-Key Navigation** for ultra-fast data entry.
  - **Auto-Capitalization** logic for clean, professional transaction records.
- **Smart Budget Alerts**: The balance card dynamically switches to "Overspent" (Red) when expenses exceed income.
- **Data Persistence**: Automatic saving and loading of transactions via JSON.
- **Full Control**: Delete confirmation dialogs and custom date selection for historical records.

## 🛠️ Built With

- **Python**: Core application logic.
- **Reflex**: An open-source framework for building full-stack web apps in pure Python.
- **Antigravity (AI Pair Programmer)**: This project was developed in a collaborative "Agentic" pair-programming environment with Antigravity, an AI assistant by Google DeepMind.

## 🎓 The Learning Journey

### How I Learnt
Building this project was a hands-on journey in **Advanced Agentic Coding**. Instead of just following a tutorial, I worked alongside an AI agent (Antigravity) to:
- **Design from scratch**: Moving from a simple concept to a professional 4-row layout.
- **Interactive Debugging**: Solving complex `AttributeError` and `SyntaxError` messages that occur in real-world development.
- **Feature Iteration**: Proposing my own ideas and seeing them come to life.

### Key Learnings
- **Reactive State Management**: Understanding how `State` variables and computed properties (`@rx.var`) drive the UI.
- **Framework Compatibility**: Learning how to adapt code to specific library versions (Reflex 0.8.26).
- **UX Strategy**: Implementing focus management and keyboard shortcuts to improve the end-user experience.
- **Data Processing**: Transforming raw transaction lists into structured data formats for interactive charts.

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [your-repo-link]
   cd finance_tracker
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   reflex run
   ```

4. **Access the App**:
   Open your browser to `http://localhost:3000`

---
*Created as part of a deep-dive into full-stack Python development.*
