import { Container, Row, Col } from 'react-bootstrap';
import InputQueryComponent from '../components/InputQueryComponent';
import AnswerQueryComponent from '../components/AnswerQueryComponent';

function QueryPage() {

    return (
        <Container 
            id="QueryPage-container"
            fluid
            className="h-100 d-flex flex-column"
        >
            <Row
                style={{
                    flex: "1 0 1",
                    minHeight: "50%",
                    maxHeight: "100%"
                }}
            >
                <Col
                    xs={6}
                    className="h-100 mx-auto"
                >
                    <AnswerQueryComponent />

                </Col>

            </Row>

            <Row
                style={{
                    flex: "1 0 auto"
                }}
            >
                <Col
                    xs={6}
                    className="h-100 mx-auto"
                >
                    <InputQueryComponent />

                </Col>

            </Row>

        </Container>
    );
}

export default QueryPage;