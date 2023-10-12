import SettingImages from "components/SettingImages";
import SettingQA from "components/SettingQA";
import { REALM_TYPES } from "constants/users";
import { useEffect } from "react";
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { AiFillSetting } from 'react-icons/ai';
import { GiArtificialIntelligence } from 'react-icons/gi';
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import Button from 'react-bootstrap/Button';


function ChatBot() {
  const account = useSelector((state) => state.account);
  const {username, role, noTabChatbot} = account;
  const navigate = useNavigate();

  useEffect(() => {
    if (!username) {
      navigate("/login");
    }
    if (username && role === REALM_TYPES.USER) {
      navigate("/");
    }
  }, [navigate, username, role]);

  return (
      <Container style={{
            "margin": "1px",
            "color": "white",
            "maxWidth": "100vw",
          }}>
        <Row>
          <Col 
            sm={2} 
            style={{
              "background": "rgb(24, 25, 26)",
              "minHeight": "80vh",
              "overflow": "auto",
              "border": "1px solid #303030",
              "borderRadius": "3px",
            }}
          >
            <Container className="p-2">
              <Button style={{"width": "100%"}} className="p-2 m-2" variant="secondary">
                <Row>
                  <Col sm={3}>
                    <AiFillSetting 
                      style={{
                        "height": "2.1rem",
                        "width": "2.1rem",
                        "borderRadius": "50%",
                      }}
                    />
                  </Col>
                  <Col sm={9}>Question & Answer</Col>
                </Row>
              </Button>
              <Button style={{"width": "100%"}} className="p-2 m-2"  variant="info">
                <Row>
                  <Col sm={3}>
                    <GiArtificialIntelligence 
                      style={{
                        "height": "2.1rem",
                        "width": "2.1rem",
                        "borderRadius": "50%",
                      }}
                    />
                  </Col>
                  <Col>Clothes Images</Col>
                </Row>
              </Button>
            </Container>
          </Col>
          <Col 
              sm={10}
              style={{
                  "background": "#00000076",
                  "border": "1px solid #303030",
                  "borderRadius": "3px"
              }}
          >
              {noTabChatbot === 0 ? (
                  <SettingQA currentChatUsername={"abc"} />
              ) : (
                  <SettingImages />
              )}
          </Col>
        </Row>
      </Container>
  );
}

export default ChatBot;
