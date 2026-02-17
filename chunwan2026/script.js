class Calculator {
    constructor() {
        this.currentOperand = '0';
        this.previousOperand = '';
        this.operation = undefined;
        this.shouldResetScreen = false;
        this.expression = '';
        
        // 魔术模式相关变量
        this.magicMode = false;
        this.equalsPressCount = 0;
        this.equalsPressTimer = null;
        this.magicInputTimer = null;
        this.magicFirstSum = null;  // 第一次运算结果 A + B
        this.magicReplacedValue = null;  // 3秒超时后替换的值 (当前时间 - magicFirstSum)
        this.magicInMultiInputPhase = false;  // 是否在多人输入阶段
        
        this.resultElement = document.getElementById('result');
        this.expressionElement = document.getElementById('expression');
        this.init();
    }

    init() {
        document.querySelectorAll('.btn').forEach(button => {
            button.addEventListener('click', () => this.handleClick(button));
        });
        
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
    }

    handleClick(button) {
        const action = button.dataset.action;
        const value = button.dataset.value;

        switch(action) {
            case 'number':
                this.appendNumber(value);
                break;
            case 'operator':
                this.chooseOperation(value);
                break;
            case 'equals':
                this.compute();
                break;
            case 'clear':
                this.clear();
                break;
            case 'backspace':
                this.backspace();
                break;
            case 'percent':
                this.percent();
                break;
            case 'decimal':
                this.appendDecimal();
                break;
            case 'negate':
                this.negate();
                break;
        }
        
        this.updateDisplay();
    }

    handleKeyboard(e) {
        if (e.key >= '0' && e.key <= '9') this.appendNumber(e.key);
        if (e.key === '.') this.appendDecimal();
        if (e.key === '=' || e.key === 'Enter') {
            e.preventDefault();
            this.compute();
        }
        if (e.key === 'Backspace') this.backspace();
        if (e.key === 'Escape') this.clear();
        if (e.key === '+' || e.key === '-' || e.key === '*' || e.key === '/') {
            this.chooseOperation(e.key);
        }
        this.updateDisplay();
    }

    appendNumber(number) {
        if (this.currentOperand === '0' || this.shouldResetScreen) {
            this.currentOperand = number;
            this.shouldResetScreen = false;
        } else {
            this.currentOperand = this.currentOperand.toString() + number.toString();
        }
        
        // 魔术模式：如果在多人输入阶段，重置超时定时器
        if (this.magicMode && this.magicInMultiInputPhase) {
            clearTimeout(this.magicInputTimer);
            this.magicInputTimer = setTimeout(() => {
                console.log('5秒超时，触发魔术替换');
                this.handleMagicTimeout();
            }, 5000);
            console.log('输入数字，重置5秒定时器');
        }
    }

    appendDecimal() {
        if (this.shouldResetScreen) {
            this.currentOperand = '0.';
            this.shouldResetScreen = false;
            return;
        }
        if (!this.currentOperand.includes('.')) {
            this.currentOperand += '.';
        }
        
        // 魔术模式：如果在多人输入阶段，重置超时定时器
        if (this.magicMode && this.magicInMultiInputPhase) {
            clearTimeout(this.magicInputTimer);
            this.magicInputTimer = setTimeout(() => {
                console.log('5秒超时，触发魔术替换');
                this.handleMagicTimeout();
            }, 5000);
            console.log('输入小数点，重置5秒定时器');
        }
    }

    chooseOperation(operation) {
        console.log('========== chooseOperation 被调用 ==========');
        console.log('operation:', operation);
        console.log('currentOperand:', this.currentOperand);
        console.log('previousOperand:', this.previousOperand);
        console.log('magicMode:', this.magicMode);
        console.log('magicFirstSum:', this.magicFirstSum);
        console.log('magicInMultiInputPhase:', this.magicInMultiInputPhase);
        console.log('==========================================');
        
        // 魔术模式特殊处理：第一次运算后按加号，进入多人输入阶段
        if (this.magicMode && operation === '+' && this.magicFirstSum !== null && !this.magicInMultiInputPhase) {
            console.log('✅ 条件满足，进入魔术模式多人输入阶段');
            this.magicInMultiInputPhase = true;
            this.operation = '+';
            this.previousOperand = this.currentOperand;  // 保存第一次运算结果
            this.shouldResetScreen = true;
            this.expression = `${this.magicFirstSum} + `;
            
            // 启动3秒超时定时器
            clearTimeout(this.magicInputTimer);
            this.magicInputTimer = setTimeout(() => {
                console.log('5秒超时，触发魔术替换');
                this.handleMagicTimeout();
            }, 5000);
            console.log('进入多人输入阶段，启动5秒定时器, timerId:', this.magicInputTimer);
            
            return;
        }
        
        console.log('❌ 魔术模式条件不满足，走正常流程');
        
        if (this.currentOperand === '') return;
        if (this.previousOperand !== '') {
            this.compute();
        }
        this.operation = operation;
        this.previousOperand = this.currentOperand;
        this.shouldResetScreen = true;
        
        const opSymbol = operation === '*' ? '×' : operation === '/' ? '÷' : operation;
        this.expression = `${this.currentOperand} ${opSymbol}`;
    }

    compute() {
        let computation;
        const prev = parseFloat(this.previousOperand);
        const current = parseFloat(this.currentOperand);
        
        console.log('========== compute 被调用 ==========');
        console.log('prev:', prev, 'current:', current);
        console.log('operation:', this.operation);
        console.log('magicMode:', this.magicMode);
        console.log('magicInMultiInputPhase:', this.magicInMultiInputPhase);
        console.log('magicFirstSum:', this.magicFirstSum);
        console.log('magicReplacedValue:', this.magicReplacedValue);
        console.log('======================================');

        // 检测连续3次等号键（必须在运算检查之前）
        this.equalsPressCount++;
        clearTimeout(this.equalsPressTimer);
        this.equalsPressTimer = setTimeout(() => {
            this.equalsPressCount = 0;
        }, 800);

        console.log('equalsPressCount:', this.equalsPressCount);

        if (this.equalsPressCount === 3) {
            console.log('🎭 触发魔术模式切换！');
            this.toggleMagicMode();
            this.equalsPressCount = 0;
            return;
        }
        
        if (isNaN(prev) && !this.magicInMultiInputPhase) {
            console.log('❌ prev 为 NaN 且不在魔术模式多人输入阶段，退出');
            return;
        }
        if (isNaN(current)) {
            console.log('❌ current 为 NaN，退出');
            return;
        }

        // 魔术模式：多人输入阶段完成最终运算
        if (this.magicMode && this.magicInMultiInputPhase) {
            console.log('=== 魔术模式最终运算 ===');
            console.log('magicFirstSum:', this.magicFirstSum);
            console.log('magicReplacedValue:', this.magicReplacedValue);
            // 取消超时定时器
            clearTimeout(this.magicInputTimer);
            // 最终结果 = 第一次运算结果 + 替换后的值
            computation = this.magicFirstSum + this.magicReplacedValue;
            console.log('最终结果:', computation);
            
            // 重置魔术模式状态
            this.magicFirstSum = null;
            this.magicReplacedValue = null;
            this.magicInMultiInputPhase = false;
        } else {
            // 正常运算或魔术模式第一次运算
            switch (this.operation) {
                case '+':
                    computation = prev + current;
                    break;
                case '-':
                    computation = prev - current;
                    break;
                case '*':
                    computation = prev * current;
                    break;
                case '/':
                    if (current === 0) {
                        this.currentOperand = 'Error';
                        this.operation = undefined;
                        this.previousOperand = '';
                        this.expression = '';
                        return;
                    }
                    computation = prev / current;
                    break;
                default:
                    return;
            }

            // 魔术模式：记录第一次运算结果
            if (this.magicMode && this.magicFirstSum === null) {
                this.magicFirstSum = computation;
                console.log('📝 记录第一次运算结果:', this.magicFirstSum);
            }
        }

        this.currentOperand = computation;
        this.operation = undefined;
        this.previousOperand = '';
        this.shouldResetScreen = true;
        this.expression = '';
    }

    clear() {
        this.currentOperand = '0';
        this.previousOperand = '';
        this.operation = undefined;
        this.expression = '';
        this.shouldResetScreen = false;
        
        // 清除魔术模式状态
        this.magicFirstSum = null;
        this.magicReplacedValue = null;
        this.magicInMultiInputPhase = false;
        clearTimeout(this.magicInputTimer);
    }

    backspace() {
        if (this.currentOperand.length === 1) {
            this.currentOperand = '0';
        } else {
            this.currentOperand = this.currentOperand.toString().slice(0, -1);
        }
    }

    percent() {
        const current = parseFloat(this.currentOperand);
        if (isNaN(current)) return;
        this.currentOperand = current / 100;
    }

    negate() {
        if (this.currentOperand === '0') return;
        this.currentOperand = (parseFloat(this.currentOperand) * -1).toString();
    }

    getDisplayNumber(number) {
        if (number === 'Error') return number;
        const stringNumber = number.toString();
        const integerDigits = parseFloat(stringNumber.split('.')[0]);
        const decimalDigits = stringNumber.split('.')[1];
        let integerDisplay;
        if (isNaN(integerDigits)) {
            integerDisplay = '';
        } else {
            integerDisplay = integerDigits.toLocaleString('en', { maximumFractionDigits: 0 });
        }
        if (decimalDigits != null) {
            return `${integerDisplay}.${decimalDigits}`;
        } else {
            return integerDisplay;
        }
    }

    updateDisplay() {
        this.resultElement.textContent = this.getDisplayNumber(this.currentOperand);
        this.expressionElement.textContent = this.expression;
    }

    // 魔术模式：获取当前时间数字 MMDDHHmm
    getCurrentTimeNumber() {
        const now = new Date();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hour = String(now.getHours()).padStart(2, '0');
        const minute = String(now.getMinutes()).padStart(2, '0');
        return parseInt(`${month}${day}${hour}${minute}`);
    }

    // 魔术模式：进入/退出
    toggleMagicMode() {
        this.magicMode = !this.magicMode;
        
        if (this.magicMode) {
            // 进入魔术模式：只改变标志，不改变屏幕数字
            console.log('🎭 魔术模式已激活！');
        } else {
            // 退出魔术模式：只改变标志，不改变屏幕数字
            this.magicFirstSum = null;
            this.magicReplacedValue = null;
            this.magicInMultiInputPhase = false;
            clearTimeout(this.magicInputTimer);
            console.log('✨ 魔术模式已关闭！');
        }
        
        this.updateDisplay();
    }

    // 魔术模式：超时处理
    handleMagicTimeout() {
        console.log('========== handleMagicTimeout 被调用 ==========');
        console.log('magicMode:', this.magicMode);
        console.log('magicInMultiInputPhase:', this.magicInMultiInputPhase);
        console.log('magicFirstSum:', this.magicFirstSum);
        console.log('================================================');
        
        if (!this.magicMode || !this.magicInMultiInputPhase) {
            console.log('❌ 条件不满足，退出');
            return;
        }
        
        // 5秒无输入，替换为当前时间减去第一次运算结果
        const timeNumber = this.getCurrentTimeNumber();
        console.log('📅 当前时间数字:', timeNumber);
        this.magicReplacedValue = timeNumber - this.magicFirstSum;
        console.log('🔄 替换后的值:', this.magicReplacedValue);
        this.currentOperand = this.magicReplacedValue.toString();
        console.log('📺 屏幕显示:', this.currentOperand);
        this.updateDisplay();
        console.log('✅ 魔术替换完成！');
    }
}

const calculator = new Calculator();
