import { Container, Row, Col } from 'react-bootstrap';
import InputQueryComponent from '../components/InputQueryComponent';
import AnswerQueryComponent from '../components/AnswerQueryComponent';

function QueryPage() {

    return (
        <Container 
            id="QueryPage-container"
            style={{ height: "100%" }}    
        >
            <Row ys={10} className="justify-content-center">
                <Col xs={8} className="justify-content-center">
                    <AnswerQueryComponent />

                </Col>

            </Row>

            <Row ys={2} className="justify-content-center">
                <Col xs={8} className="justify-content-center">
                    <InputQueryComponent />

                </Col>

            </Row>

        </Container>
    );
}

export default QueryPage;