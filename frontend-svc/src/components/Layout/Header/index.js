import { Container, Nav, Navbar, NavDropdown } from "react-bootstrap";
import styles from "./Header.module.scss";
import { LinkContainer } from "react-router-bootstrap";
import { connect } from "react-redux";
import { VscAccount } from "react-icons/vsc";
import { HiOutlineBookOpen } from "react-icons/hi";
import { AiOutlineGlobal } from "react-icons/ai";
import { useTranslation } from "react-i18next";
import { useState } from "react";

function Header(props) {
  const { dispatch, account } = props;
  const { t, i18n } = useTranslation();
  const [lang, setLang] = useState(localStorage.getItem("lang") || "EN");
  const listLanguages = [
    {
      name: "EN",
      key: "en",
    },
    {
      name: "VI",
      key: "vi",
    },
  ];
  const changeLanguage = (language) => {
    const curLang = listLanguages.find((item) => item.key === language);
    setLang(curLang.name);
    i18n.changeLanguage(language);
    localStorage.setItem("lang", curLang.name)
  };
  return (
    <Navbar className={styles["navbar-header"]}>
      <Container style={{ maxWidth: "100%" }}>
        <Navbar.Collapse id="responsive-navbar-nav" className={styles["navbar-collapse"]}>
          <Nav className={styles["navbar-docs"]}>
            <NavDropdown
              title={
                <div className={styles["nav-header-item"]}>
                  <AiOutlineGlobal className={styles["header-icon"]} /> {lang}{" "}
                </div>
              }
              id="navbarScrollingDropdown"
              className={styles["nav-header-item"]}
            >
              {listLanguages.map((lang, index) => (
                <NavDropdown.Item
                  onClick={() => changeLanguage(lang.key)}
                  key={index}
                  className={styles["dropdown-item"]}
                >
                  <span>{lang.name}</span>
                </NavDropdown.Item>
              ))}
            </NavDropdown>
            {props.username && (
              <LinkContainer to="/documents">
                <Nav.Link
                  active={false}
                  className={`${styles["nav-item"]} ${styles["nav-header-item"]}`}
                >
                  <HiOutlineBookOpen className={styles["header-icon"]} />
                  {t("head.document")}
                </Nav.Link>
              </LinkContainer>
            )}
          </Nav>
          <Nav className={styles["navbar-account"]}>
            {props.username && (
              <NavDropdown
                title={
                  <div className={styles["nav-header-item"]}>
                    <VscAccount className={styles["header-icon"]} /> {props.username}{" "}
                  </div>
                }
                id="navbarScrollingDropdown"
                className={styles["nav-header-item"]}
              >
                <LinkContainer to="/profile">
                  <NavDropdown.Item className={styles["dropdown-item"]}>
                    <div>
                      <span>{t("title.profile")}</span>
                    </div>
                  </NavDropdown.Item>
                </LinkContainer>
                <LinkContainer to="/account-management">
                  <NavDropdown.Item className={styles["dropdown-item"]}>
                    <div>
                      <span>{t("title.accountManagement")}</span>
                    </div>
                  </NavDropdown.Item>
                </LinkContainer>
                <div
                  onClick={() => {
                    dispatch({ type: "account/handleSignOut" });
                  }}
                >
                  <NavDropdown.Item className={styles["dropdown-item"]}>
                    <div>
                      <span>{t("title.signout")}</span>
                    </div>
                  </NavDropdown.Item>
                </div>
              </NavDropdown>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

const mapStateToProps = (state) => ({
  account: state.account,
});

export default connect(mapStateToProps)(Header);
