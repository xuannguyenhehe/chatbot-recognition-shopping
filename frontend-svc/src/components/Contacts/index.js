import defaultAvatar from "assets/DefaultAvatar.png";
import React, { useState } from "react";
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { AiFillSetting } from 'react-icons/ai';
import { GiArtificialIntelligence } from 'react-icons/gi';
import { IoIosContact } from 'react-icons/io';
import { SiChatbot } from 'react-icons/si';
import { useDispatch, useSelector } from "react-redux";


const Contacts = ({ chats, contacts, changeChat, handleTabChange, noTab }) => {
  const dispatch = useDispatch();
  const account = useSelector((state) => state.account);
  const {username} = account;

  const [currentSelected, setCurrentSelected] = useState("");

  const changeTab = (index) => {
    dispatch({
      type: "account/saveState",
      payload: {
        noTab: index,
      },
    });
    handleTabChange(index);
  }

  const changeCurrentChat = (index, contact) => {
    setCurrentSelected(index);
    changeChat(contact);
  };

  return (
    <>
      <Container className="p-0">
        <Row style={{"height": "75vh"}}>
          <Container>
          {noTab === 0 && contacts.map((contact, index) => {
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
                    <h6>{contact.name}</h6>
                  </Col>
                </Row>
              );
            })}
            {noTab === 1 && chats.map((contact, index) => {
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
                    <h5>{contact.name}</h5>
                    <h6>{contact.last_message_user === username ? "Me:" : contact.last_message_user} {contact.last_message}</h6>
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
            "textAlign": "center",
          }}
          className="p-2"
        >
          <Col sm={6}>
            <IoIosContact 
              style={{
                "height": "3.1rem",
                "width": "3.1rem",
                "borderRadius": "50%",
                "color": noTab === 0 ? "blue" : "white",
              }}
              onClick={() => changeTab(0)}
            />
          </Col>
          <Col sm={6}>
            <SiChatbot 
              style={{
                "height": "3.1rem",
                "width": "3.1rem",
                "borderRadius": "50%",
                "color": noTab === 1 ? "blue" : "white",
              }}
              onClick={() => changeTab(1)}
            />
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default Contacts;
