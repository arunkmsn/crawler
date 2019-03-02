import React, { Component } from "react";
import "./App.css";
import Crawl from "./crawl_btn";
import Url from "./url";
import Depth from "./depth";
import ImageGal from "./image_gallery";

const API_SERVER="http://" + window.location.hostname + ":8000";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      url: "",
      depth: 0,
      job_id: "",
      result: ""
    };
  }

  componentDidMount() {
    
  }

  checkResult() {
    if (this.state.job_id !== "") {
      console.log("checking for results...");
      fetch(API_SERVER + "/status/" + this.state.job_id)
      .then(response => response.text())
      .then(data => {if (data === "SUCCESS") this.fetchResults(); else console.log("not ready yet: " + data)})
      .catch(error => console.error(error));
    }
  }

  fetchResults() {
    console.log("Found results... Clearing interval...");
    clearInterval(this.interval_id);
    fetch(API_SERVER + "/results/" + this.state.job_id)
    .then(response => response.json())
    .then(json => this.setState({
      result: json, 
      job_id: "",
      job_in_progress: false
    }))
    .catch(error => console.error(error));
  }

  submitJob(e) {
    console.log("Started submit job");
    if (!this.state.job_in_progress) {
      this.setState({ job_in_progress: true });
      var formData = new FormData();
      formData.append("url", this.state.url);
      formData.append("depth", this.state.depth);

      fetch(API_SERVER + "/crawl", {
        method: "POST",
        body: formData,
        cache: "no-cache"
      }).then(response => response.json())
        .then(json => {
          this.setState({job_id: json});
          this.interval_id = setInterval(() => this.checkResult(), 5000, json);
        })
        .catch(error => console.error(error));
    } else {
      console.log("Job running...");
    }
  }

  urlChange(e) {
    this.setState({
      url: e.target.value,
      result: ""
    });
  }

  depthChange(e) {
    this.setState({
      depth: e.target.value,
      result: ""
    });
  }

  render() {
    return (
      <div className="container mt-5 pt-5">
        <h1>Crawler</h1>
        <Url onChange={e => this.urlChange(e)} value={this.state.url} />
        <Depth onChange={e => this.depthChange(e)} value={this.state.depth} />
        <Crawl
          onClick={e => this.submitJob(e)}
          acceptInput={!this.state.job_in_progress && this.state.url !== "" && parseInt(this.state.depth) > 0}
        />
        <ImageGal result={this.state.result} jobRunning={this.state.job_in_progress} />
      </div>
    );
  }
}

export default App;
