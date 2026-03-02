import React from 'react';
import { ListGroup, Button, Spinner } from 'react-bootstrap';
import type { Dialog } from '../types/QueryPageTypes';

interface DialogsListProps {
  dialogs: Dialog[];
  currentDialogId?: number;
  onSelectDialog: (dialogId: number) => void;
  onCreateDialog: () => void;
  loading?: boolean;
}

const DialogsList: React.FC<DialogsListProps> = ({
  dialogs,
  currentDialogId,
  onSelectDialog,
  onCreateDialog,
  loading = false,
}) => {
  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', borderRight: '1px solid #dee2e6' }}>
      <div style={{ padding: '1rem', borderBottom: '1px solid #dee2e6' }}>
        <Button variant="primary" onClick={onCreateDialog} disabled={loading} className="w-100">
          + Новый диалог
        </Button>
      </div>
      <div style={{ flex: 1, overflowY: 'auto' }}>
        {loading && dialogs.length === 0 ? (
          <div className="d-flex justify-content-center mt-4">
            <Spinner animation="border" variant="primary" />
          </div>
        ) : dialogs.length === 0 ? (
          <p className="text-muted text-center mt-4">Нет диалогов</p>
        ) : (
          <ListGroup variant="flush">
            {dialogs.map((dialog) => (
              <ListGroup.Item
                key={dialog.dialog_id}
                action
                active={dialog.dialog_id === currentDialogId}
                onClick={() => onSelectDialog(dialog.dialog_id)}
                style={{ cursor: 'pointer' }}
              >
                <div className="d-flex justify-content-between align-items-center">
                  <span>Диалог #{dialog.dialog_id}</span>
                  <small className="text-muted">
                    {new Date(dialog.created_at).toLocaleDateString()}
                  </small>
                </div>
              </ListGroup.Item>
            ))}
          </ListGroup>
        )}
      </div>
    </div>
  );
};

export default DialogsList;