import { Container } from "react-bootstrap";


function AnswerQueryComponent() {
    const longText = "Здесь ваш длинный текст... ".repeat(10);

    return (
        <Container id="AnswerQueryComponent-container">
            <div style={{ marginTop: '60px' }}>
                <h1>Длинный текст</h1>
                <p>{longText}</p>
            </div>
        </Container>
    );
}

export default AnswerQueryComponent;