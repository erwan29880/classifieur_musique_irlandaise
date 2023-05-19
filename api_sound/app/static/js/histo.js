function genLoss(data){
    return {'type': 'line',
                "data": {
                    "labels": data['index'],
                    "datasets": [
                        {
                            "data" : data["loss"],
                            "type":"line",
                            "fill":"true",
                            "borderWidth":2,
                            "pointRadius": 3,
                            "pointHoverRadius": 3,
                            "backgroundColor":"blue",
                            "borderColor": "blue",
                            "label":"loss"
                        },
                        {
                            "data" : data["val_loss"],
                            "type":"line",
                            "fill":"true",
                            "borderWidth":2,
                            "pointRadius": 3,
                            "pointHoverRadius": 3,
                            "backgroundColor":"orange",
                            "borderColor": "orange",
                            "label":"val_loss"
                        }
                    ]
                },
                "options": {
                            "responsive": "true",
                            "interaction":{"intersect":"true",
                                        "mode":"index"
                                        },
                            "plugins": {
                                "title": {
                                    "display": "true",
                                    "text": "loss" 
                                },
                                "legend": { 
                                    "display": "true",
                                    "position": "bottom" 
                                }
                            },
                            "scales": {
                                "y": {
                                    "display":"false",
                                    "ticks": {
                                        "min": 0,
                                        "beginAtZero": "true"
                                        },
                                    "title":{
                                        "display": "true",
                                        "text": "crossentropy"
                                    },
                                    "min":0
                                },
                            "x": {
                                    "display":"true",
                                    "ticks": {
                                        "min": 0,
                                        "beginAtZero": "true"
                                        },
                                    "title":{
                                        "display": "true",
                                        "text": "epochs"
                                    }
                                }
                            }
                    }
                };
}



function genPrecision(data){
    return {'type': 'line',
            "data": {
                "labels": data['index'],
                "datasets": [
                    {
                        "data" : data["precision"],
                        "type":"line",
                        "fill":"true",
                        "borderWidth":2,
                        "pointRadius": 3,
                        "pointHoverRadius": 3,
                        "backgroundColor":"blue",
                        "borderColor": "blue",
                        "label":"precision"
                    },
                    {
                        "data" : data["val_precision"],
                        "type":"line",
                        "fill":"true",
                        "borderWidth":2,
                        "pointRadius": 3,
                        "pointHoverRadius": 3,
                        "backgroundColor":"orange",
                        "borderColor": "orange",
                        "label":"val_precision"
                    }
                ]
            },
            "options": {
                        "responsive": "false",
                        "interaction":{"intersect":"true",
                                    "mode":"index"
                                    },
                        "plugins": {
                            "title": {
                                "display": "true",
                                "text": "précision" 
                            },
                            "legend": { 
                                "display": "true",
                                "position": "bottom" 
                            }
                        },
                        "scales": {
                            "y": {
                                "display":"true",
                                "ticks": {
                                    "min": 0,
                                    "beginAtZero": "true"
                                    },
                                "title":{
                                    "display": "true",
                                    "text": "%"
                                },
                                "min":0,
                                "max":100
                            },
                        "x": {
                                "display":"true",
                                "ticks": {
                                    "min": 0,
                                    "beginAtZero": "true"
                                    },
                                "title":{
                                    "display": "true",
                                    "text": "epochs"
                                }
                            }
                        }
                }
            };
}


function genRecall(data){
    return {'type': 'line',
            "data": {
                "labels": data['index'],
                "datasets": [
                    {
                        "data" : data["recall"],
                        "type":"line",
                        "fill":"true",
                        "borderWidth":2,
                        "pointRadius": 3,
                        "pointHoverRadius": 3,
                        "backgroundColor":"blue",
                        "borderColor": "blue",
                        "label":"recall"
                    },
                    {
                        "data" : data["val_recall"],
                        "type":"line",
                        "fill":"true",
                        "borderWidth":2,
                        "pointRadius": 3,
                        "pointHoverRadius": 3,
                        "backgroundColor":"orange",
                        "borderColor": "orange",
                        "label":"val_recall"
                    }
                ]
            },
            "options": {
                        "responsive": "false",
                        "interaction":{"intersect":"true",
                                    "mode":"index"
                                    },
                        "plugins": {
                            "title": {
                                "display": "true",
                                "text": "recall" 
                            },
                            "legend": { 
                                "display": "true",
                                "position": "bottom" 
                            }
                        },
                        "scales": {
                            "y": {
                                "display":"true",
                                "ticks": {
                                    "min": 0,
                                    "beginAtZero": "true"
                                    },
                                "title":{
                                    "display": "true",
                                    "text": "%"
                                },
                                "min":0,
                                "max":100
                            },
                        "x": {
                                "display":"true",
                                "ticks": {
                                    "min": 0,
                                    "beginAtZero": "true"
                                    },
                                "title":{
                                    "display": "true",
                                    "text": "epochs"
                                }
                            }
                        }
                }
            };
}


