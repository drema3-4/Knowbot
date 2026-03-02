import React, { useState, useEffect } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import InputQueryComponent from '../components/InputQueryComponent';
import AnswerQueryComponent from '../components/AnswerQueryComponent';
import DialogsList from '../components/DialogsList';
import { useUser } from '../context/UserContext';
import { fetchUserDialogs, createDialog, fetchDialogMessages } from '../services/DialogApi';
import type { Dialog, Message } from '../types/QueryPageTypes';

const QueryPage: React.FC = () => {
  const { user } = useUser();
  const [dialogs, setDialogs] = useState<Dialog[]>([]);
  const [currentDialogId, setCurrentDialogId] = useState<number | undefined>();
  const [messages, setMessages] = useState<Message[]>([]);
  const [loadingDialogs, setLoadingDialogs] = useState(false);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [sending, setSending] = useState(false);

  // Загружаем диалоги при наличии пользователя
  useEffect(() => {
    if (!user) return;

    const loadDialogs = async () => {
      setLoadingDialogs(true);
      try {
        const userDialogs = await fetchUserDialogs(user.user_id);
        setDialogs(userDialogs);
        // Если есть диалоги, можно выбрать первый? Пока не выбираем, оставляем currentDialogId undefined.
      } catch (error) {
        console.error('Ошибка загрузки диалогов:', error);
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
      try {
        const dialogMessages = await fetchDialogMessages(currentDialogId, user.user_id);
        setMessages(dialogMessages);
      } catch (error) {
        console.error('Ошибка загрузки сообщений:', error);
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

    try {
      const newDialog = await createDialog(user.user_id);
      setDialogs(prev => [newDialog, ...prev]); // добавляем в начало
      setCurrentDialogId(newDialog.dialog_id); // сразу выбираем новый диалог
      setMessages([]); // очищаем сообщения (новый диалог пуст)
    } catch (error) {
      console.error('Ошибка создания диалога:', error);
    }
  };

  const handleSend = async (question: string) => {
    // Пока заглушка – просто логируем и добавляем сообщение пользователя (без ответа)
    // Позже здесь будет вызов /api/v1/query
    console.log('Отправка сообщения:', question);

    // Добавляем сообщение пользователя (временное, без ответа)
    const tempUserMessage: Message = {
      id: Date.now().toString(),
      text: question,
      sender: 'user',
    };
    setMessages(prev => [...prev, tempUserMessage]);

    // Здесь пока нет ответа от бота – нужно будет доработать на следующем этапе
    // Если нет текущего диалога, нужно сначала создать его
    if (!currentDialogId) {
      // TODO: создать диалог и затем отправить сообщение
      console.warn('Нет выбранного диалога. Сначала создайте или выберите диалог.');
    }
  };

  // Определяем, можно ли отправлять сообщения: есть пользователь и выбран диалог
  const canSend = !!user && !!currentDialogId && !sending;

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