import { Container } from "react-bootstrap";


function AnswerQueryComponent() {
    const longText = "Здесь ваш длинный текст... ".repeat(2);

    return (
        <Container
            id="AnswerQueryComponent-container"
            className="h-100 d-flex flex-column"
        >
            <div
                style={{
                    overflowY: "auto",
                    marginTop: "60px"
                }}
            >
                <h1>Длинный текст</h1>
                <p>{longText}</p>
            </div>
        </Container>
    );
}

export default AnswerQueryComponent;