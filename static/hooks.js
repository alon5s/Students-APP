function Div(props) {

    const [news, setNews] = React.useState(["Welcome!"]);

    const getData = () => {
        axios.get("/message").then(response => {
            setNews(response.data);
        })
    }

    React.useEffect(() => {
        setInterval(getData, props.interval);
    }, []
    )

    return (
        <div>
            {news.map((item) =>
                <h3>{item}</h3>
            )}
        </div>
    );
}

// בונוס: הרשימה תהיה מוגבלת ל 5 הודעות, כשנכנסת הודעה חדשה היא מופיעה ראשונה והאחרונה נעלמת.

ReactDOM.render(<Div interval={3000} />, document.getElementById("message"));