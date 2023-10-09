import React from "react";
import { useNavigate } from "react-router-dom";
import Card from "react-bootstrap/Card";
import { TbAlignLeft } from "react-icons/tb";
import Loading from "components/CircleLoading";
import styles from "./WrapLayout.module.scss";

function WrapLayout({ breadCrumb, children, loading }) {
  const navigate = useNavigate();
  return (
    <div className={styles.wrapLayout}>
      {loading && <Loading />}
      <Card className={styles.card}>
        <Card.Header className={styles.cardHeader}>
          <TbAlignLeft className={styles.breadCrumbIcon} />
          {breadCrumb.map((item, index) => (
            <div key={index}>
              <h4
                className={`${styles.link} ${styles.linkRoot}`}
                onClick={() => navigate(item.path)}
              >
                {item.name}
              </h4>
              {index !== breadCrumb.length - 1 && (
                <h4 className={styles.iconRefix}>{`>>`}</h4>
              )}
            </div>
          ))}
        </Card.Header>
        <Card.Body className={styles.cardBody}>{children}</Card.Body>
      </Card>
    </div>
  );
}

export default WrapLayout;
