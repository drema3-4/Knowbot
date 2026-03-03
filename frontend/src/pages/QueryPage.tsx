import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Alert } from 'react-bootstrap';
import InputQueryComponent from '../components/InputQueryComponent';
import AnswerQueryComponent from '../components/AnswerQueryComponent';
import DialogsList from '../components/DialogsList';
import { useUser } from '../context/UserContext';
import { fetchUserDialogs, createDialog, fetchDialogMessages } from '../services/DialogApi';
import { sendMessage } from '../services/QueryPageApi';
import type { Dialog, Message } from '../types/QueryPageTypes';

const QueryPage: React.FC = () => {
  const { user } = useUser();
  const [dialogs, setDialogs] = useState<Dialog[]>([]);
  const [currentDialogId, setCurrentDialogId] = useState<number | undefined>();
  const [messages, setMessages] = useState<Message[]>([]);
  const [loadingDialogs, setLoadingDialogs] = useState(false);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Загружаем диалоги при наличии пользователя
  useEffect(() => {
    if (!user) return;

    const loadDialogs = async () => {
      setLoadingDialogs(true);
      setError(null);
      try {
        const userDialogs = await fetchUserDialogs(user.user_id);
        setDialogs(userDialogs);
      } catch (error) {
        console.error('Ошибка загрузки диалогов:', error);
        setError('Не удалось загрузить диалоги');
      } finally {
        setLoadingDialogs(false);
      }
    };

    loadDialogs();
  }, [user]);

  // Загружаем сообщения при выборе диалога
  useEffect(() => {
    if (!user || !currentDialogId) {
      setMessages([]); // очищаем сообщения, если диалог не выбран
      return;
    }

    const loadMessages = async () => {
      setLoadingMessages(true);
      setError(null);
      try {
        const dialogMessages = await fetchDialogMessages(currentDialogId, user.user_id);
        setMessages(dialogMessages);
      } catch (error) {
        console.error('Ошибка загрузки сообщений:', error);
        setError('Не удалось загрузить сообщения');
        setMessages([]);
      } finally {
        setLoadingMessages(false);
      }
    };

    loadMessages();
  }, [currentDialogId, user]);

  const handleSelectDialog = (dialogId: number) => {
    setCurrentDialogId(dialogId);
  };

  const handleCreateDialog = async () => {
    if (!user) return;
    setError(null);
    try {
      const newDialog = await createDialog(user.user_id);
      setDialogs(prev => [newDialog, ...prev]); // добавляем в начало
      setCurrentDialogId(newDialog.dialog_id); // сразу выбираем новый диалог
      setMessages([]); // очищаем сообщения (новый диалог пуст)
    } catch (error) {
      console.error('Ошибка создания диалога:', error);
      setError('Не удалось создать диалог');
    }
  };

  const handleSend = async (question: string) => {
    if (!user) return;

    // Если нет текущего диалога, сначала создаём его
    let targetDialogId = currentDialogId;
    if (!targetDialogId) {
      setSending(true);
      try {
        const newDialog = await createDialog(user.user_id);
        setDialogs(prev => [newDialog, ...prev]);
        targetDialogId = newDialog.dialog_id;
        setCurrentDialogId(targetDialogId);
      } catch (error) {
        console.error('Ошибка создания диалога перед отправкой:', error);
        setError('Не удалось создать диалог');
        setSending(false);
        return;
      }
    }

    // Добавляем временное сообщение пользователя
    const tempUserMessage: Message = {
      id: 'temp-' + Date.now().toString(),
      text: question,
      sender: 'user',
    };
    setMessages(prev => [...prev, tempUserMessage]);
    setSending(true);
    setError(null);

    try {
      // Отправляем запрос к /api/v1/query
      // const botMessage = await sendMessage(question, user.user_id, targetDialogId);
      await sendMessage(question, user.user_id, targetDialogId);

      // Заменяем временное сообщение пользователя на постоянное?
      // Но на бэкенде оно уже сохранилось, поэтому мы можем просто добавить ответ бота
      // и при желании обновить список сообщений, но у нас уже есть пользовательское сообщение.
      // Лучше перезагрузить сообщения диалога, чтобы получить актуальную историю.
      // Однако для простоты добавим ответ бота и удалим временное сообщение? Нет, лучше перезагрузить.

      // Перезагружаем сообщения текущего диалога, чтобы получить обновлённую историю
      if (targetDialogId) {
        const updatedMessages = await fetchDialogMessages(targetDialogId, user.user_id);
        setMessages(updatedMessages);
      }
    } catch (error) {
      console.error('Ошибка отправки сообщения:', error);
      setError('Не удалось отправить сообщение');
      // Удаляем временное сообщение пользователя (так как оно не сохранилось)
      setMessages(prev => prev.filter(msg => msg.id !== tempUserMessage.id));
    } finally {
      setSending(false);
    }
  };

  // Определяем, можно ли отправлять сообщения: есть пользователь и не отправляется сейчас
  const canSend = !!user && !sending;

  return (
    <Container fluid style={{ height: '100%', padding: 0 }}>
      <Row style={{ height: '100%', margin: 0 }}>
        {/* Левая колонка – список диалогов */}
        <Col xs={12} md={4} lg={3} style={{ padding: 0, height: '100%' }}>
          <DialogsList
            dialogs={dialogs}
            currentDialogId={currentDialogId}
            onSelectDialog={handleSelectDialog}
            onCreateDialog={handleCreateDialog}
            loading={loadingDialogs}
          />
        </Col>

        {/* Правая колонка – чат */}
        <Col xs={12} md={8} lg={9} style={{ padding: 0, height: '100%', display: 'flex', flexDirection: 'column' }}>
          {error && (
            <Alert variant="danger" dismissible onClose={() => setError(null)} className="m-2">
              {error}
            </Alert>
          )}
          {loadingMessages ? (
            <div className="d-flex justify-content-center align-items-center" style={{ flex: 1 }}>
              Загрузка сообщений...
            </div>
          ) : (
            <>
              <div style={{ flex: 1, overflow: 'hidden' }}>
                <AnswerQueryComponent messages={messages} />
              </div>
              <div style={{ borderTop: '1px solid #ccc', backgroundColor: '#fff' }}>
                <InputQueryComponent onSend={handleSend} disabled={!canSend} />
              </div>
              {!currentDialogId && user && (
                <div style={{ textAlign: 'center', padding: '0.5rem', color: '#6c757d' }}>
                  Выберите или создайте диалог, чтобы начать общение.
                </div>
              )}
            </>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default QueryPage;