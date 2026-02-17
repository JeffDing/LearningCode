// 计算器状态
let currentValue = '0';
let previousValue = '';
let operation = null;
let shouldResetScreen = false;
let lastEqualsPressTime = 0;
let equalsPressCount = 0;
let isLocked = false;
let lockedValue = 0;

const resultScreen = document.getElementById('result');
const expressionScreen = document.getElementById('expression');

// 获取当前时间格式化为MMDDHHmm
function getCurrentTimeValue() {
    const now = new Date();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hour = String(now.getHours()).padStart(2, '0');
    const minute = String(now.getMinutes()).padStart(2, '0');
    return parseInt(month + day + hour + minute);
}

// 格式化数字显示
function formatNumber(num) {
    if (num === 'Error') return num;
    const str = num.toString();
    if (str.length > 12) {
        return parseFloat(num).toExponential(6);
    }
    return str;
}

// 更新显示屏
function updateDisplay() {
    resultScreen.textContent = formatNumber(currentValue);
    if (operation) {
        expressionScreen.textContent = `${formatNumber(previousValue)} ${operation}`;
    } else {
        expressionScreen.textContent = '';
    }
}

// 处理数字输入
function handleNumber(num) {
    if (shouldResetScreen) {
        currentValue = num;
        shouldResetScreen = false;
    } else {
        if (currentValue === '0' && num !== '.') {
            currentValue = num;
        } else if (currentValue.replace(/[^0-9]/g, '').length < 12) {
            currentValue += num;
        }
    }
    updateDisplay();
}

// 处理小数点
function handleDecimal() {
    if (shouldResetScreen) {
        currentValue = '0.';
        shouldResetScreen = false;
    } else if (!currentValue.includes('.')) {
        currentValue += '.';
    }
    updateDisplay();
}

// 处理删除
function handleDelete() {
    if (currentValue.length === 1) {
        currentValue = '0';
    } else {
        currentValue = currentValue.slice(0, -1);
    }
    updateDisplay();
}

// 处理清除
function handleClear() {
    currentValue = '0';
    previousValue = '';
    operation = null;
    shouldResetScreen = false;
    updateDisplay();
}

// 处理百分号
function handlePercent() {
    currentValue = (parseFloat(currentValue) / 100).toString();
    updateDisplay();
}

// 处理运算符
function handleOperator(op) {
    if (operation !== null && !shouldResetScreen) {
        calculate();
    }
    previousValue = currentValue;
    operation = op;
    shouldResetScreen = true;
    updateDisplay();
}

// 计算结果
function calculate() {
    if (operation === null || shouldResetScreen) return;
    
    let result;
    const prev = parseFloat(previousValue);
    const current = parseFloat(currentValue);
    
    if (isNaN(prev) || isNaN(current)) return;
    
    switch (operation) {
        case '+':
            result = prev + current;
            break;
        case '-':
            result = prev - current;
            break;
        case '*':
            result = prev * current;
            break;
        case '/':
            if (current === 0) {
                result = 'Error';
            } else {
                result = prev / current;
            }
            break;
        default:
            return;
    }
    
    currentValue = result.toString();
    operation = null;
    previousValue = '';
    shouldResetScreen = true;
    updateDisplay();
}

// 处理等号键（包含锁定/解锁逻辑）
function handleEquals() {
    const now = Date.now();
    
    // 检查是否在500ms内连续点击
    if (now - lastEqualsPressTime < 500) {
        equalsPressCount++;
    } else {
        equalsPressCount = 1;
    }
    
    lastEqualsPressTime = now;
    
    // 连续点击3次等号键
    if (equalsPressCount === 3) {
        if (!isLocked) {
            // 进入锁定状态
            isLocked = true;
            lockedValue = parseFloat(currentValue) || 0;
            console.log('已锁定，锁定值:', lockedValue);
        } else {
            // 解除锁定状态
            isLocked = false;
            const currentTimeValue = getCurrentTimeValue();
            const result = currentTimeValue - lockedValue;
            currentValue = result.toString();
            operation = null;
            previousValue = '';
            shouldResetScreen = true;
            console.log('已解锁，当前时间:', currentTimeValue, '锁定值:', lockedValue, '结果:', result);
        }
        equalsPressCount = 0;
        updateDisplay();
        return;
    }
    
    // 正常计算
    calculate();
}

// 添加事件监听器
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', () => {
        const action = button.dataset.action;
        const value = button.dataset.value;
        
        switch (action) {
            case 'number':
                handleNumber(value);
                break;
            case 'operator':
                handleOperator(value);
                break;
            case 'decimal':
                handleDecimal();
                break;
            case 'clear':
                handleClear();
                break;
            case 'backspace':
                handleDelete();
                break;
            case 'percent':
                handlePercent();
                break;
            case 'equals':
                handleEquals();
                break;
        }
    });
});

// 键盘支持
document.addEventListener('keydown', (e) => {
    if (e.key >= '0' && e.key <= '9') {
        handleNumber(e.key);
    } else if (e.key === '.') {
        handleDecimal();
    } else if (e.key === '+') {
        handleOperator('+');
    } else if (e.key === '-') {
        handleOperator('-');
    } else if (e.key === '*') {
        handleOperator('*');
    } else if (e.key === '/') {
        handleOperator('/');
    } else if (e.key === 'Enter' || e.key === '=') {
        handleEquals();
    } else if (e.key === 'Backspace') {
        handleDelete();
    } else if (e.key === 'Escape') {
        handleClear();
    } else if (e.key === '%') {
        handlePercent();
    }
});
