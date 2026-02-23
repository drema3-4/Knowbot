import { Container } from 'react-bootstrap';
import InputQueryComponent from '../components/InputQueryComponent';
import AnswerQueryComponent from '../components/AnswerQueryComponent';
import mockMessages from './mockMessage.json';

function QueryPage() {
  const hasMessages = mockMessages.length > 0;

  return (
    <div style={{ height: '100vh', position: 'relative' }}>
      {hasMessages ? (
        // Стандартный вид: список сверху, поле снизу
        <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
          <div style={{ flex: 1, overflow: 'hidden' }}>
            <AnswerQueryComponent messages={mockMessages} />
          </div>
          <div style={{ borderTop: '1px solid #ccc' }}>
            <InputQueryComponent />
          </div>
        </div>
      ) : (
        // Пустой чат: поле по центру
        <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <InputQueryComponent />
        </div>
      )}
    </div>
  );
}

export default QueryPage;