import "../Layout.scss";
import Header from "../Header";

function Layout(props) {
  return (
    <div>
      <Header username={props.username} role={props.role} />
      <main className="w-100" style={{height: "calc(100vh - var(--header-height))"}}>{props.children}</main>
    </div>
  );
}

export default Layout;
