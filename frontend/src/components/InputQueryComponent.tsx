import { useState } from "react";
import TextareaAutosize from 'react-textarea-autosize';

function InputQueryComponent() {
    const [inputValue, setInputValue] = useState('');

    return (
        <TextareaAutosize
            minRows={2}
            maxRows={8}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Введите сюда свой запрос..."
        >

        </TextareaAutosize>
    );
}

export default InputQueryComponent;