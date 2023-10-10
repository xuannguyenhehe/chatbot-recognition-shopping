import defaultAvatar from "assets/DefaultAvatar.png";
import React, { useState } from "react";
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { AiFillSetting } from 'react-icons/ai';
import { GiArtificialIntelligence } from 'react-icons/gi';
import { IoIosContact } from 'react-icons/io';
import { SiChatbot } from 'react-icons/si';

const Contacts = ({ contacts, changeChat }) => {
  const [currentSelected, setCurrentSelected] = useState("");

  const changeCurrentChat = (index, contact) => {
    setCurrentSelected(index);
    changeChat(contact);
  };

  return (
    <>
      <Container className="p-0">
        <Row style={{"height": "80vh"}}>
          <Container>
            {contacts.map((contact, index) => {
              return (
                <Row 
                  key={contact._id}
                  className={`contact m-3 ${index === currentSelected ? "selected" : ""}`}
                  onClick={() => changeCurrentChat(index, contact)}
                >
                  <Col sm={3} style={{"width": "20%"}}>
                    <img src={contact.avatarImage || defaultAvatar} alt="" style={{"height": "3.1rem"}} />
                  </Col>
                  <Col sm={9}>
                    <Row>{contact.name}</Row>
                    <Row>Text message...</Row>
                  </Col>
                </Row>
              );
            })}
          </Container>
        </Row>
        <Row 
          style={{
            "backgroundColor": "#18191a",
            "borderTop": "0.2px solid #ffffff15",
          }}
          className="p-2"
        >
          <Col sm={3}>
            <IoIosContact 
              style={{
                "height": "3.1rem",
                "width": "3.1rem",
                "borderRadius": "50%",
              }}
            />
          </Col>
          <Col sm={3}>
            <SiChatbot 
              style={{
                "height": "3.1rem",
                "width": "3.1rem",
                "borderRadius": "50%",
              }}
            />
          </Col>
          <Col sm={3}>
            <GiArtificialIntelligence 
              style={{
                "height": "3.1rem",
                "width": "3.1rem",
                "borderRadius": "50%",
              }}
            />
          </Col>
          <Col sm={3}>
            <AiFillSetting 
              style={{
                "height": "3.1rem",
                "width": "3.1rem",
                "borderRadius": "50%",
              }}
            />
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default Contacts;
