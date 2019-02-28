import React, { Component } from "react";

class Crawl extends Component {
  render() {
    if (this.props.acceptInput) {
      return (
        <div className="form-group">
          <button
            className="form-control col-md-3 btn  btn-primary"
            onClick={() => this.props.onClick()}
          >
            Crawl
          </button>
        </div>
      );
    } else {
      return (
        <div className="form-group">
          <button className="form-control col-md-3 btn  btn-primary" disabled>
            Crawl
          </button>
        </div>
      );
    }
  }
}

export default Crawl;
