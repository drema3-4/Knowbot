import { Container, Row, Col, Button } from 'react-bootstrap';

function App() {

    return (
        <Container>
            <Row className='justify-content-center' sytle={{marginTop: '6em'}}>
                <Col xs={5} className='justify-content-center'>
                    <Button variant="primary">Primary</Button>
                </Col>
            </Row>
        </Container>
    )
}

export default App