import { Container, Form, Row, Button } from "react-bootstrap";
import { useState } from "react";

function InputQueryComponent() {
    const [inputValue, setInputValue] = useState('');

    return (
        <Container
            id="InputQueryComponent-container"
            className="h-100"
        >
            <Form
                className="d-flex flex-column"
                style={{
                    backgroundColor: "white",
                    padding: "15px",
                    borderRadius: "8px",
                    boxShadow: "0 2px 10px rgba(0,0,0,0.1)"
                }}
            >
                <Row
                    style={{
                        flex: "1 1 1"
                    }}
                >
                    <Form.Control
                        as="textarea"
                        type="text"
                        placeholder="Введите запрос"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        style={{
                            resize: "vertical",
                            overflowY: "auto",
                            whiteSpace: "pre-wrap",
                            wordWrap: "break-word",
                            lineHeight: "1.5"
                        }}
                        
                    />
                    
                </Row>
                <Row
                    style={{
                        flex: "0 0 auto"
                    }}
                >
                    <Button variant="primary" type="submit">
                        Submit
                    </Button>

                </Row>
            </Form>

        </Container>
    );
}

export default InputQueryComponent;