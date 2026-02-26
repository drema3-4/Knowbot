// pages/QueryPage.tsx
import InputQueryComponent from '../components/InputQueryComponent';
import AnswerQueryComponent from '../components/AnswerQueryComponent';
import { useState } from 'react';
// import { useEffect, useState } from 'react';
import type { Message } from '../types/QueryPageTypes';
import { sendMessage } from '../services/QueryPageApi';
// import { fetchHistory, sendMessage } from '../services/QueryPageApi';

function QueryPage() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [loading, setLoading] = useState(false);

    // useEffect(() => {
    //     fetchHistory()
    //         .then(setMessages)
    //         .catch(console.error);
    // }, []);

    const handleSend = async (prompt: string) => {
        const userMessage: Message = {
            id: Date.now().toString(),
            text: prompt,
            sender: 'user'
        };
        setMessages(prev => [...prev, userMessage]);
        setLoading(true);

        try {
            const botMessage = await sendMessage(prompt);
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error('Ошибка при отправке: ', error);
        } finally {
            setLoading(false);
        }
    };

    const hasMessages = messages.length > 0;

    return (
        <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
            <div style={{ flex: '1 1 auto', overflow: 'hidden' }}>
                {hasMessages ? (
                    <AnswerQueryComponent messages={messages} />
                ) : (
                    <div
                        style={{
                            height: '100%',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            flexDirection: 'column',
                            textAlign: 'center',
                            padding: '20px',
                        }}
                    >
                        <h2>Добро пожаловать в чат с AI</h2>
                        <p className="text-muted">Задайте любой вопрос, чтобы начать</p>
                    </div>
                )}
            </div>

            <div style={{ flexShrink: 0, borderTop: '1px solid #ccc', backgroundColor: '#fff', width: '100%' }}>
                <InputQueryComponent onSend={handleSend} disabled={loading} />
            </div>
        </div>
    );
}

export default QueryPage;