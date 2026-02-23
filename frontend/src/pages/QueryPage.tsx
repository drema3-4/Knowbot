import InputQueryComponent from '../components/InputQueryComponent';
import AnswerQueryComponent from '../components/AnswerQueryComponent';
import mockMessages from './mockMessage.json';

function QueryPage() {
  const hasMessages = mockMessages.length > 0;

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Верхняя часть: либо список сообщений, либо приветствие */}
      <div style={{ flex: '1 1 auto', overflow: 'hidden' }}>
        {hasMessages ? (
          <AnswerQueryComponent messages={mockMessages} />
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

      {/* Нижняя часть: поле ввода */}
      <div style={{ flexShrink: 0, borderTop: '1px solid #ccc', backgroundColor: '#fff', width: '100%' }}>
        <InputQueryComponent />
      </div>
    </div>
  );
}

export default QueryPage;