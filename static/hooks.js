function Messages(props) {

    const [message, setMessage] = React.useState(["Welcome!"]);

    const getData = () => {
        axios.get("/message").then(response => {
            setMessage(response.data);
        })
    }

    React.useEffect(() => {
        setInterval(getData, props.interval);
    }, []
    )

    return (
        <div>
            {message.map((item) =>
                <h3>{item}</h3>
            )}
        </div>
    );
}

// בונוס: הרשימה תהיה מוגבלת ל 5 הודעות, כשנכנסת הודעה חדשה היא מופיעה ראשונה והאחרונה נעלמת.

ReactDOM.render(<Messages interval={3000} />, document.getElementById("message"));