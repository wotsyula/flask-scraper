import axios from 'axios';
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import Person from './Person';
import { findPeopleResults } from '../redux/actions/peopleActions';

const PeopleResults = () => {
    const dispatch = useDispatch();
    const people = useSelector((state) => state.people);
    const results = [];
    const status = people.status;

    // Poll for results
    useEffect(() => {
        // Exit early if not running
        if (!status) return;

        const timer = setInterval(() => axios
            .get('http://localhost:5000/api/v1/scraper/google/findpeople/results')
            .then((response) => {
                dispatch(findPeopleResults(response.data));
            })
            .catch((err) => {
                console.log(err);
            })

        , 10000);

        return () => clearInterval(timer);
    });

    for (let url in people.byUrl) {
        results.push(<Person url={url} text={people.byUrl[url]} key={url} />)
    }

    if (results.length < 1) {
        results.push(
            <div className="content">
                <span key="data:" className="description">No Results</span>
            </div>
        );
    }

    return (
        <div className="ui grid container">
            <div className="ui cards">
                {results.map((v) => (
                    <div key={v.key} className="card">
                            {v}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default PeopleResults;
