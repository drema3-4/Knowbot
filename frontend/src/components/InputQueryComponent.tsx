import { useState } from "react";
import type { KeyboardEvent } from "react";
import TextareaAutosize from 'react-textarea-autosize';

interface InputQueryComponentProps {
    onSend: (message: string) => void;
    disabled?: boolean;
}

function InputQueryComponent({ onSend, disabled = false }: InputQueryComponentProps) {
    const [inputValue, setInputValue] = useState('');

    const handleSend = () => {
        if (inputValue.trim() && !disabled) {
            onSend(inputValue.trim());
            setInputValue('');
        }
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault(); // предотвращаем перевод строки
            handleSend();
        }
    };

    return (
        <div style={{ width: '100%', display: 'flex', justifyContent: 'center', padding: '0.75rem 1rem', gap: '0.5rem' }}>
            <TextareaAutosize
                minRows={2}
                maxRows={8}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Введите сюда свой запрос..."
                disabled={disabled}
                style={{
                    width: '100%',
                    maxWidth: '800px',
                    resize: 'none',
                    padding: '0.5rem',
                    borderRadius: '8px',
                    border: '1px solid #ccc',
                }}
            />
            <button
                onClick={handleSend}
                disabled={disabled || !inputValue.trim()}
                style={{
                    padding: '0.5rem 1rem',
                    borderRadius: '8px',
                    border: 'none',
                    backgroundColor: '#007bff',
                    color: 'white',
                    cursor: 'pointer',
                    alignSelf: 'flex-end',
                    marginBottom: '0.25rem',
                }}
            >
                Отправить
            </button>
        </div>
    );
}

export default InputQueryComponent;