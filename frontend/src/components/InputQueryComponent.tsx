import { Container, Form, Row, Col, Button } from "react-bootstrap";
import { useState } from "react";

function InputQueryComponent() {
    const [inputValue, setInputValue] = useState('');

    return (
        <Container
            id="InputQueryComponent-container"
            style={{
                backgroundColor: "white",
                padding: "15px",
                borderRadius: "8px",
                boxShadow: "0 2px 10px rgba(0,0,0,0.1)"
            }}
        >
            <Form>
                <Row>
                    <Col xs={10}>
                        <Form.Control
                            type="text"
                            placeholder="Введите запрос"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                        />
                    </Col>
                    <Col xs={2}>
                        <Button variant="primary" type="submit">
                            Submit
                        </Button>
                    </Col>
                </Row>
            </Form>
        </Container>
    );
}

export default InputQueryComponent;