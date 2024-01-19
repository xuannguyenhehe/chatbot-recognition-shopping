import "./Layout.scss";
import Header from "./Header";
import Footer from "./Footer";

function Layout(props) {
  return (
    <div style={{"backgroundColor": "#0e0e11"}}>
      <Header username={props.username} />
      <div style={{"height": "52rem"}}>
        {props.children}
      </div>
      <Footer />
    </div>
  );
}

export default Layout;
