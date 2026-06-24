/* @ds-bundle: {"format":3,"namespace":"TPOGroupDesignSystem_479b56","components":[],"sourceHashes":{"ui_kits/website/Bars.jsx":"315edc2ae152","ui_kits/website/Button.jsx":"7b4c7aac7196","ui_kits/website/Contact.jsx":"d033664c219b","ui_kits/website/Field.jsx":"a1a2b903df48","ui_kits/website/Footer.jsx":"3f4e60d51c83","ui_kits/website/Header.jsx":"6def4ae89475","ui_kits/website/Hero.jsx":"7898aa4708ba","ui_kits/website/Icon.jsx":"2ff2f2f3bd2b","ui_kits/website/Pillars.jsx":"c5d19697ac11","ui_kits/website/Services.jsx":"ae46c0129e38"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.TPOGroupDesignSystem_479b56 = window.TPOGroupDesignSystem_479b56 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// ui_kits/website/Bars.jsx
try { (() => {
/* global React */
function Bars({
  height = 110,
  gap = 6,
  opacity = 1
}) {
  // 14 bars, varying heights, green→teal→blue spectrum
  const bars = [{
    h: 0.62,
    c: "#06371F"
  }, {
    h: 0.82,
    c: "#0F5E36"
  }, {
    h: 0.50,
    c: "#0E8E54"
  }, {
    h: 0.96,
    c: "#0C9C7B"
  }, {
    h: 0.66,
    c: "#0E8FA8"
  }, {
    h: 1.00,
    c: "#1378B8"
  }, {
    h: 0.86,
    c: "#1A6BC9"
  }, {
    h: 0.54,
    c: "#185BB0"
  }, {
    h: 0.76,
    c: "#0E8FA8"
  }, {
    h: 0.46,
    c: "#0C9C7B"
  }, {
    h: 0.82,
    c: "#0E8E54"
  }, {
    h: 0.64,
    c: "#0F5E36"
  }, {
    h: 0.40,
    c: "#06371F"
  }, {
    h: 0.72,
    c: "#0C9C7B"
  }];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "flex-end",
      gap,
      height,
      opacity
    }
  }, bars.map((b, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      width: 8,
      height: `${b.h * 100}%`,
      background: b.c,
      borderRadius: 9999
    }
  })));
}
window.Bars = Bars;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Bars.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/Button.jsx
try { (() => {
/* global React, Icon */
const buttonBase = {
  fontFamily: "inherit",
  fontWeight: 700,
  fontSize: 14,
  letterSpacing: "0.02em",
  padding: "13px 24px",
  border: "1px solid transparent",
  cursor: "pointer",
  borderRadius: 2,
  transition: "all 200ms cubic-bezier(.2,.6,.2,1)",
  textDecoration: "none",
  display: "inline-flex",
  alignItems: "center",
  gap: 10,
  lineHeight: 1
};
function Button({
  variant = "primary",
  children,
  onClick,
  withArrow
}) {
  const [hover, setHover] = React.useState(false);
  const palette = {
    primary: {
      background: hover ? "#0E8E54" : "#06371F",
      color: "#fff"
    },
    secondary: {
      background: "#fff",
      color: hover ? "#0E8E54" : "#06371F",
      borderColor: hover ? "#0E8E54" : "#06371F"
    },
    ghost: {
      background: "transparent",
      color: hover ? "#0E8E54" : "#06371F"
    },
    onDark: {
      background: hover ? "#0E8E54" : "#fff",
      color: hover ? "#fff" : "#06371F"
    }
  }[variant];
  return /*#__PURE__*/React.createElement("button", {
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      ...buttonBase,
      ...palette
    }
  }, children, withArrow && /*#__PURE__*/React.createElement(Icon, {
    name: "arrow-right",
    size: 16
  }));
}
window.Button = Button;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Button.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/Contact.jsx
try { (() => {
/* global React, Field, Button, Icon */
function Contact() {
  const [data, setData] = React.useState({
    first: "",
    last: "",
    email: "",
    message: ""
  });
  const [sent, setSent] = React.useState(false);
  const set = k => e => setData({
    ...data,
    [k]: e.target.value
  });
  return /*#__PURE__*/React.createElement("section", {
    style: {
      background: "#fff",
      padding: "120px 40px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1280,
      margin: "0 auto",
      display: "grid",
      gridTemplateColumns: "1fr 1.2fr",
      gap: 80
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      fontWeight: 700,
      letterSpacing: ".14em",
      textTransform: "uppercase",
      color: "#0E8E54",
      marginBottom: 18
    }
  }, "Contact"), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontFamily: "Newsreader, Georgia, serif",
      fontVariationSettings: '"opsz" 48',
      fontWeight: 600,
      fontSize: 44,
      letterSpacing: "-0.02em",
      lineHeight: 1.05,
      color: "#06371F",
      margin: "0 0 22px"
    }
  }, "To inquire about our services, please contact us below."), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 16,
      lineHeight: 1.65,
      color: "#3B4A42",
      margin: "0 0 36px"
    }
  }, "We reply to qualified inquiries within one business day. For active incidents, call the hotline directly."), /*#__PURE__*/React.createElement("ul", {
    style: {
      listStyle: "none",
      padding: 0,
      margin: 0,
      display: "flex",
      flexDirection: "column",
      gap: 16
    }
  }, /*#__PURE__*/React.createElement("li", {
    style: {
      display: "flex",
      gap: 12,
      alignItems: "center",
      color: "#0B0F0D"
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "mail",
    size: 20,
    color: "#06371F"
  }), /*#__PURE__*/React.createElement("a", {
    href: "mailto:info@tpo.group",
    style: {
      color: "inherit",
      textDecoration: "none",
      fontSize: 15.5
    }
  }, "info@tpo.group")), /*#__PURE__*/React.createElement("li", {
    style: {
      display: "flex",
      gap: 12,
      alignItems: "center",
      color: "#0B0F0D"
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "phone",
    size: 20,
    color: "#06371F"
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 15.5,
      fontFamily: "JetBrains Mono, monospace"
    }
  }, "855.787.4370")), /*#__PURE__*/React.createElement("li", {
    style: {
      display: "flex",
      gap: 12,
      alignItems: "flex-start",
      color: "#3B4A42"
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "map-pin",
    size: 20,
    color: "#06371F"
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 14,
      lineHeight: 1.55
    }
  }, "Boston \xB7 New York \xB7 Washington \xB7 Seattle", /*#__PURE__*/React.createElement("br", null), "Austin \xB7 San Francisco \xB7 London")))), /*#__PURE__*/React.createElement("div", {
    style: {
      background: "#F6F8F6",
      border: "1px solid rgba(11,15,13,.10)",
      padding: 40
    }
  }, sent ? /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: "center",
      padding: "40px 0"
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "shield-check",
    size: 48,
    color: "#0E8E54"
  }), /*#__PURE__*/React.createElement("h3", {
    style: {
      fontFamily: "Newsreader, Georgia, serif",
      fontVariationSettings: '"opsz" 32',
      fontSize: 24,
      color: "#06371F",
      margin: "16px 0 8px",
      fontWeight: 600,
      letterSpacing: "-0.01em"
    }
  }, "Thanks for submitting."), /*#__PURE__*/React.createElement("p", {
    style: {
      color: "#3B4A42",
      margin: 0
    }
  }, "A member of the team will be in touch within one business day.")) : /*#__PURE__*/React.createElement("form", {
    onSubmit: e => {
      e.preventDefault();
      setSent(true);
    },
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      gap: 14
    }
  }, /*#__PURE__*/React.createElement(Field, {
    label: "First Name",
    value: data.first,
    onChange: set("first")
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Last Name",
    value: data.last,
    onChange: set("last")
  })), /*#__PURE__*/React.createElement(Field, {
    label: "Email",
    type: "email",
    value: data.email,
    onChange: set("email")
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Message",
    as: "textarea",
    value: data.message,
    onChange: set("message")
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 8
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    withArrow: true
  }, "Send"))))));
}
window.Contact = Contact;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Contact.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/Field.jsx
try { (() => {
/* global React */
function Field({
  label,
  type = "text",
  as = "input",
  value,
  onChange,
  placeholder
}) {
  const [focus, setFocus] = React.useState(false);
  const baseStyle = {
    fontFamily: "inherit",
    width: "100%",
    padding: "12px 14px",
    border: `1px solid ${focus ? "#06371F" : "rgba(11,15,13,.18)"}`,
    background: "#fff",
    fontSize: 14,
    color: "#0B0F0D",
    borderRadius: 2,
    boxSizing: "border-box",
    outline: "none",
    transition: "border-color 200ms",
    boxShadow: focus ? "0 0 0 3px rgba(14,142,84,.16)" : "none",
    resize: as === "textarea" ? "vertical" : undefined,
    minHeight: as === "textarea" ? 96 : undefined
  };
  const Tag = as;
  return /*#__PURE__*/React.createElement("label", {
    style: {
      display: "block"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: "block",
      fontSize: 12,
      letterSpacing: ".04em",
      textTransform: "uppercase",
      color: "#3B4A42",
      marginBottom: 6,
      fontWeight: 600
    }
  }, label), /*#__PURE__*/React.createElement(Tag, {
    type: type,
    value: value || "",
    onChange: onChange,
    placeholder: placeholder,
    style: baseStyle,
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false)
  }));
}
window.Field = Field;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Field.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/Footer.jsx
try { (() => {
/* global React, Bars */
function Footer() {
  return /*#__PURE__*/React.createElement("footer", {
    style: {
      background: "#042B1B",
      color: "#B7C5BD",
      paddingTop: 80
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1280,
      margin: "0 auto",
      padding: "0 40px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1.3fr 1fr 1fr 1fr",
      gap: 40,
      paddingBottom: 56,
      borderBottom: "1px solid rgba(255,255,255,.10)"
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/logos/tpo-logo-white-emerald.png",
    alt: "TPO.group",
    style: {
      height: 32,
      marginBottom: 22
    }
  }), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 13.5,
      lineHeight: 1.65,
      margin: 0,
      maxWidth: 320
    }
  }, "Mission-critical cybersecurity consulting for critical infrastructure, government agencies, and the enterprises that depend on them.")), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h4", {
    style: {
      fontSize: 11,
      letterSpacing: ".14em",
      color: "#fff",
      textTransform: "uppercase",
      margin: "0 0 14px",
      fontWeight: 700
    }
  }, "Practice"), /*#__PURE__*/React.createElement("ul", {
    style: {
      listStyle: "none",
      padding: 0,
      margin: 0,
      fontSize: 13.5,
      lineHeight: 2
    }
  }, /*#__PURE__*/React.createElement("li", null, "Services"), /*#__PURE__*/React.createElement("li", null, "Team"), /*#__PURE__*/React.createElement("li", null, "News"), /*#__PURE__*/React.createElement("li", null, "Contact"))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h4", {
    style: {
      fontSize: 11,
      letterSpacing: ".14em",
      color: "#fff",
      textTransform: "uppercase",
      margin: "0 0 14px",
      fontWeight: 700
    }
  }, "Trust"), /*#__PURE__*/React.createElement("ul", {
    style: {
      listStyle: "none",
      padding: 0,
      margin: 0,
      fontSize: 13.5,
      lineHeight: 2
    }
  }, /*#__PURE__*/React.createElement("li", null, "Security"), /*#__PURE__*/React.createElement("li", null, "Privacy Policy"), /*#__PURE__*/React.createElement("li", null, "Vulnerability Disclosure"))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h4", {
    style: {
      fontSize: 11,
      letterSpacing: ".14em",
      color: "#fff",
      textTransform: "uppercase",
      margin: "0 0 14px",
      fontWeight: 700
    }
  }, "Contact"), /*#__PURE__*/React.createElement("ul", {
    style: {
      listStyle: "none",
      padding: 0,
      margin: 0,
      fontSize: 13.5,
      lineHeight: 2
    }
  }, /*#__PURE__*/React.createElement("li", null, "info@tpo.group"), /*#__PURE__*/React.createElement("li", {
    style: {
      fontFamily: "JetBrains Mono, monospace"
    }
  }, "855.787.4370")))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "flex-end",
      padding: "40px 0 32px",
      gap: 40,
      flexWrap: "wrap"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12,
      letterSpacing: ".14em",
      textTransform: "uppercase",
      color: "rgba(255,255,255,.55)"
    }
  }, "Boston \xB7 New York \xB7 Washington \xB7 Seattle \xB7 Austin \xB7 San Francisco \xB7 London"), /*#__PURE__*/React.createElement(Bars, {
    height: 56,
    gap: 5,
    opacity: 0.85
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      borderTop: "1px solid rgba(255,255,255,.10)",
      padding: "20px 0 28px",
      fontSize: 11,
      letterSpacing: ".14em",
      textTransform: "uppercase",
      color: "rgba(255,255,255,.45)"
    }
  }, "\xA9 2025 TPO.GROUP \xA0\xB7\xA0 TECHNOLOGY \xB7 POLICY \xB7 OPERATIONS")));
}
window.Footer = Footer;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Footer.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/Header.jsx
try { (() => {
/* global React */
function Header({
  route,
  setRoute
}) {
  const [scrolled, setScrolled] = React.useState(false);
  React.useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  const navItems = [{
    id: "services",
    label: "Services"
  }, {
    id: "team",
    label: "Team"
  }, {
    id: "news",
    label: "News"
  }, {
    id: "contact",
    label: "Contact"
  }];
  return /*#__PURE__*/React.createElement("header", {
    style: {
      position: "sticky",
      top: 0,
      zIndex: 50,
      background: scrolled ? "rgba(255,255,255,0.82)" : "#fff",
      backdropFilter: scrolled ? "blur(12px)" : "none",
      borderBottom: scrolled ? "1px solid rgba(11,15,13,.10)" : "1px solid transparent",
      transition: "all 200ms cubic-bezier(.2,.6,.2,1)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1280,
      margin: "0 auto",
      padding: "18px 40px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between"
    }
  }, /*#__PURE__*/React.createElement("a", {
    href: "#",
    onClick: e => {
      e.preventDefault();
      setRoute("home");
    },
    style: {
      display: "inline-flex"
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/logos/tpo-logo.png",
    alt: "TPO.group",
    style: {
      height: 36
    }
  })), /*#__PURE__*/React.createElement("nav", {
    style: {
      display: "flex",
      gap: 32
    }
  }, navItems.map(it => {
    const active = route === it.id;
    return /*#__PURE__*/React.createElement("a", {
      key: it.id,
      href: "#",
      onClick: e => {
        e.preventDefault();
        setRoute(it.id);
      },
      style: {
        fontSize: 14,
        fontWeight: 600,
        letterSpacing: ".01em",
        color: active ? "#0E8E54" : "#0B0F0D",
        textDecoration: "none",
        padding: "8px 0",
        borderBottom: active ? "2px solid #0E8E54" : "2px solid transparent",
        transition: "all 200ms"
      }
    }, it.label);
  })), /*#__PURE__*/React.createElement("a", {
    href: "#",
    onClick: e => {
      e.preventDefault();
      setRoute("contact");
    },
    style: {
      fontSize: 13,
      fontWeight: 700,
      letterSpacing: ".02em",
      padding: "10px 20px",
      background: "#06371F",
      color: "#fff",
      textDecoration: "none",
      borderRadius: 2
    }
  }, "Get a briefing")));
}
window.Header = Header;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Header.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/Hero.jsx
try { (() => {
/* global React, Bars, Button */
function Hero({
  setRoute
}) {
  return /*#__PURE__*/React.createElement("section", {
    style: {
      background: "#042B1B",
      color: "#F4F7F5",
      position: "relative",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1280,
      margin: "0 auto",
      padding: "120px 40px 140px",
      position: "relative",
      zIndex: 2
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      fontWeight: 700,
      letterSpacing: ".14em",
      textTransform: "uppercase",
      color: "#3CBE85",
      marginBottom: 28
    }
  }, "Technology \xB7 Policy \xB7 Operations"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontFamily: "Newsreader, Georgia, serif",
      fontVariationSettings: '"opsz" 72',
      fontWeight: 600,
      fontSize: "clamp(40px,5.4vw,72px)",
      lineHeight: 1.04,
      letterSpacing: "-0.022em",
      color: "#fff",
      maxWidth: 1040,
      margin: "0 0 32px"
    }
  }, "TPO Group leads in ", /*#__PURE__*/React.createElement("em", {
    style: {
      fontStyle: "italic",
      fontWeight: 500,
      color: "#3CBE85"
    }
  }, "mission\u2011critical, high\u2011stakes"), " cybersecurity consulting through strategic experience and technical prowess."), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 19,
      lineHeight: 1.6,
      color: "#B7C5BD",
      maxWidth: 720,
      margin: "0 0 40px"
    }
  }, "Our custom solutions and incident response targeted training ensure operational continuity and security amid evolving cyber threats."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 12
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "onDark",
    withArrow: true,
    onClick: () => setRoute("services")
  }, "View Our Services"), /*#__PURE__*/React.createElement(Button, {
    variant: "ghost",
    onClick: () => setRoute("contact")
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: "#F4F7F5"
    }
  }, "Request a briefing")))), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      right: 40,
      bottom: 0,
      opacity: 0.55,
      pointerEvents: "none"
    }
  }, /*#__PURE__*/React.createElement(Bars, {
    height: 170,
    gap: 8
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      left: 0,
      right: 0,
      bottom: 0,
      height: 1,
      background: "rgba(255,255,255,.10)"
    }
  }));
}
window.Hero = Hero;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Hero.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/Icon.jsx
try { (() => {
/* global React */
const {
  useState
} = React;

/* -------------------------------------------------------------------------- */
/*  Icon  — light wrapper for inline Lucide-style SVG. Stroke 1.5, rounded.   */
/* -------------------------------------------------------------------------- */
function Icon({
  name,
  size = 28,
  color = "currentColor",
  strokeWidth = 1.5
}) {
  const paths = {
    "shield-check": /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("path", {
      d: "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "m9 12 2 2 4-4"
    })),
    "scale": /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("path", {
      d: "m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M7 21h10"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M12 3v18"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"
    })),
    "siren": /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("path", {
      d: "M7 18v-6a5 5 0 1 1 10 0v6"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M5 21a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M21 21a1 1 0 0 1-1-1v-2a1 1 0 0 1 1-1h-1a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1z",
      transform: "translate(0)"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M21 12h1"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M18.5 4.5 18 5"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M2 12h1"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M12 2v1"
    }), /*#__PURE__*/React.createElement("path", {
      d: "m4.929 4.929.707.707"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M12 12v6"
    })),
    "compass": /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("circle", {
      cx: "12",
      cy: "12",
      r: "10"
    }), /*#__PURE__*/React.createElement("polygon", {
      points: "16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"
    })),
    "cloud": /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("path", {
      d: "M17.5 19a4.5 4.5 0 1 0-1.42-8.78A6 6 0 0 0 4 12.5 4.5 4.5 0 0 0 6.5 19h11Z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M12 12v6"
    }), /*#__PURE__*/React.createElement("path", {
      d: "m9 15 3-3 3 3"
    })),
    "network": /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("rect", {
      x: "16",
      y: "16",
      width: "6",
      height: "6",
      rx: "1"
    }), /*#__PURE__*/React.createElement("rect", {
      x: "2",
      y: "16",
      width: "6",
      height: "6",
      rx: "1"
    }), /*#__PURE__*/React.createElement("rect", {
      x: "9",
      y: "2",
      width: "6",
      height: "6",
      rx: "1"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M12 12V8"
    })),
    "graduation": /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("path", {
      d: "M22 10v6"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M2 10l10-5 10 5-10 5z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M6 12v5c3 3 9 3 12 0v-5"
    })),
    "cpu": /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("rect", {
      x: "4",
      y: "4",
      width: "16",
      height: "16",
      rx: "2"
    }), /*#__PURE__*/React.createElement("rect", {
      x: "9",
      y: "9",
      width: "6",
      height: "6"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M15 2v2"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M15 20v2"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M2 15h2"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M2 9h2"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M20 15h2"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M20 9h2"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M9 2v2"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M9 20v2"
    })),
    "user-x": /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("path", {
      d: "M14.5 21H3a4 4 0 0 1 4-4h4"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "10",
      cy: "7",
      r: "4"
    }), /*#__PURE__*/React.createElement("path", {
      d: "m17 17 5 5"
    }), /*#__PURE__*/React.createElement("path", {
      d: "m22 17-5 5"
    })),
    "menu": /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("line", {
      x1: "4",
      y1: "6",
      x2: "20",
      y2: "6"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "4",
      y1: "12",
      x2: "20",
      y2: "12"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "4",
      y1: "18",
      x2: "20",
      y2: "18"
    })),
    "arrow-right": /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("line", {
      x1: "5",
      y1: "12",
      x2: "19",
      y2: "12"
    }), /*#__PURE__*/React.createElement("polyline", {
      points: "12 5 19 12 12 19"
    })),
    "mail": /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("rect", {
      x: "2",
      y: "4",
      width: "20",
      height: "16",
      rx: "2"
    }), /*#__PURE__*/React.createElement("path", {
      d: "m22 7-10 7L2 7"
    })),
    "phone": /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("path", {
      d: "M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"
    })),
    "map-pin": /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("path", {
      d: "M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "12",
      cy: "10",
      r: "3"
    }))
  };
  return /*#__PURE__*/React.createElement("svg", {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: color,
    strokeWidth: strokeWidth,
    strokeLinecap: "round",
    strokeLinejoin: "round",
    "aria-hidden": "true"
  }, paths[name] || null);
}
window.Icon = Icon;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Icon.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/Pillars.jsx
try { (() => {
/* global React */
const PILLAR_DATA = [{
  name: "TECHNOLOGY",
  body: "Our cloud security design services ensure organizations can modernize their infrastructure while maintaining security and compliance standards. We specialize in complex migration scenarios that require maintaining operational continuity while enhancing security posture."
}, {
  name: "POLICY",
  body: "360-degree security strategy creation spanning program design, policy development, governance structure, framework/standards mapping, and metrics that deliver a singular goal: assuring clients' operational efficiency and business growth."
}, {
  name: "OPERATIONS",
  body: "Elite Incident Response assuring containment and eradication of advanced adversaries on compromised networks, identification of human threats, and recommended actions to thwart related attack vectors and tighten business continuity and disaster recovery."
}];
function Pillars() {
  return /*#__PURE__*/React.createElement("section", {
    style: {
      background: "#fff",
      padding: "120px 40px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1280,
      margin: "0 auto"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(3, 1fr)",
      gap: 48,
      alignItems: "start"
    }
  }, PILLAR_DATA.map((p, i) => /*#__PURE__*/React.createElement("article", {
    key: p.name
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "JetBrains Mono, monospace",
      fontSize: 12,
      color: "#82918A",
      marginBottom: 18
    }
  }, "0", i + 1, " / 03"), /*#__PURE__*/React.createElement("div", {
    style: {
      width: 48,
      height: 3,
      background: "#0E8E54",
      marginBottom: 22
    }
  }), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontFamily: "Hanken Grotesk, sans-serif",
      fontWeight: 800,
      fontSize: 28,
      letterSpacing: ".08em",
      color: "#06371F",
      margin: "0 0 20px",
      lineHeight: 1.1
    }
  }, p.name), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 15.5,
      lineHeight: 1.7,
      color: "#3B4A42",
      margin: 0
    }
  }, p.body))))));
}
window.Pillars = Pillars;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Pillars.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/Services.jsx
try { (() => {
/* global React, Icon */
const SERVICES = [{
  icon: "shield-check",
  title: "Resilience Growth Strategy",
  body: "Bespoke, 360-degree security strategy spanning program design, policy development, governance, standards mapping, and metrics."
}, {
  icon: "scale",
  title: "vCISO",
  body: "Executive partnership that forges a prioritized roadmap to achieve client business goals and meet regulatory demands."
}, {
  icon: "siren",
  title: "Incident Response",
  body: "Containment and eradication of adversaries on compromised networks, identification of human threats and recommended actions to thwart related attack vectors and strengthen business continuity and recovery."
}, {
  icon: "compass",
  title: "Policy Navigation",
  body: "Customized roadmaps to navigate global policy, inform internal practices, and shape future policy collaboratively with industry and government."
}, {
  icon: "cloud",
  title: "Cloud Security Architecture Services",
  body: "Complex migration and optimization that maintain operational continuity and enhance security posture."
}, {
  icon: "network",
  title: "Digital Supply Chain Risk Management",
  body: "An architectural approach for comprehensive security across interconnected business ecosystems."
}, {
  icon: "graduation",
  title: "Executive Education",
  body: "Strategic and tactical uplift to security teams spanning 360 degree risk management and incident response."
}, {
  icon: "cpu",
  title: "SOC Enhancement",
  body: "We tune existing tools, augment threat intelligence, and meaningfully integrate artificial intelligence."
}, {
  icon: "user-x",
  title: "Insider Threat Management",
  body: "Reviewing or designing insider threat programs, focusing on identification, assessment, monitoring and removal of insider risks. Leading or advising on insider risk investigations."
}];
function ServiceCard({
  icon,
  title,
  body
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("article", {
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      background: "#fff",
      border: "1px solid rgba(11,15,13,.18)",
      borderLeft: `3px solid ${hover ? "#0E8E54" : "transparent"}`,
      padding: "32px 30px 34px",
      display: "flex",
      flexDirection: "column",
      gap: 14,
      transition: "all 200ms cubic-bezier(.2,.6,.2,1)",
      boxShadow: hover ? "0 1px 2px rgba(11,15,13,.04),0 1px 3px rgba(11,15,13,.06)" : "none",
      cursor: "pointer"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      color: "#06371F"
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: icon,
    size: 40
  })), /*#__PURE__*/React.createElement("h3", {
    style: {
      fontFamily: "Newsreader, Georgia, serif",
      fontVariationSettings: '"opsz" 32',
      fontWeight: 600,
      fontSize: 22,
      color: "#06371F",
      margin: "8px 0 0",
      letterSpacing: "-0.012em",
      lineHeight: 1.2
    }
  }, title), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14.5,
      lineHeight: 1.65,
      color: "#3B4A42",
      margin: 0
    }
  }, body));
}
function ServicesGrid({
  withHero = false
}) {
  return /*#__PURE__*/React.createElement("section", {
    style: {
      background: "#F6F8F6",
      padding: "120px 40px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1280,
      margin: "0 auto"
    }
  }, withHero && /*#__PURE__*/React.createElement("header", {
    style: {
      marginBottom: 64,
      maxWidth: 820
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      fontWeight: 700,
      letterSpacing: ".14em",
      textTransform: "uppercase",
      color: "#0E8E54",
      marginBottom: 18
    }
  }, "What we do"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontFamily: "Newsreader, Georgia, serif",
      fontVariationSettings: '"opsz" 60',
      fontWeight: 600,
      fontSize: "clamp(36px,4.4vw,56px)",
      letterSpacing: "-0.02em",
      lineHeight: 1.05,
      color: "#06371F",
      margin: "0 0 18px"
    }
  }, "Cybersecurity for a ", /*#__PURE__*/React.createElement("em", {
    style: {
      fontStyle: "italic",
      fontWeight: 500,
      color: "#0E8E54"
    }
  }, "Safer Future")), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 19,
      lineHeight: 1.6,
      color: "#3B4A42",
      margin: 0
    }
  }, "TPO Group specializes in cyber defense for complex, high-stakes environments, including critical infrastructure and government agencies.")), !withHero && /*#__PURE__*/React.createElement("header", {
    style: {
      marginBottom: 48
    }
  }, /*#__PURE__*/React.createElement("h2", {
    style: {
      fontFamily: "Newsreader, Georgia, serif",
      fontVariationSettings: '"opsz" 48',
      fontWeight: 600,
      fontSize: 44,
      letterSpacing: "-0.018em",
      color: "#06371F",
      margin: 0,
      lineHeight: 1.05
    }
  }, "Our Services")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(3, 1fr)",
      gap: 0,
      borderTop: "1px solid rgba(11,15,13,.10)",
      borderLeft: "1px solid rgba(11,15,13,.10)"
    }
  }, SERVICES.map(s => /*#__PURE__*/React.createElement("div", {
    key: s.title,
    style: {
      borderRight: "1px solid rgba(11,15,13,.10)",
      borderBottom: "1px solid rgba(11,15,13,.10)"
    }
  }, /*#__PURE__*/React.createElement(ServiceCard, s))))));
}
window.ServicesGrid = ServicesGrid;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Services.jsx", error: String((e && e.message) || e) }); }

})();
