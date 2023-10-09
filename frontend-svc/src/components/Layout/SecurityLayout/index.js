import logo from "assets/logo/logo_vts.png";
import { Card, Col, Container, Row, Image } from "react-bootstrap";
import Loading from "components/CircleLoading";
import { useTranslation } from "react-i18next";
function Security(props) {
  const {t} = useTranslation()
  return (
    <Container style={{height: "100%"}}>
      {props.isLoading && <Loading />}
      <Row style={{height: "100%", alignItems: "center"}}>
        <Col sm={8}>
          <Image fluid src={logo} alt="background" />
        </Col>
        <Col sm={4}>
          <Card className="border m-3">
            <Card.Body>
              <Card.Title className="m-3 fs-3 fw-bold text-center">
                {t("title.login")}
              </Card.Title>
              {props.children}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default Security;
