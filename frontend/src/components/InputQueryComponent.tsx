import { useState } from "react";
import TextareaAutosize from 'react-textarea-autosize';

function InputQueryComponent() {
    const [inputValue, setInputValue] = useState('');

    return (
        <div style={{ width: '100%', display: 'flex', justifyContent: 'center', padding: '0.75rem 1rem' }}>
            <TextareaAutosize
                minRows={2}
                maxRows={8}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Введите сюда свой запрос..."
                style={{ width: '100%', maxWidth: '800px', resize: 'none' }}
            />
        </div>
    );
}

export default InputQueryComponent;