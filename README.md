# wids-deauth-detection-
# Wi-Fi Deauthentication Flood Detection (WIDS)

A simple wireless intrusion detection prototype that uses a Random Forest classifier to label Wi-Fi packets as normal or deauthentication-flood attack traffic. When an attack packet is detected, it prints an alert and simulates a response action.

## How it works
1. Load two CSV files: normal traffic and deauthentication attack traffic.
2. Label each packet (0 = normal, 1 = attack) and combine the files.
3. Select three numeric features.
4. Split the data 70% training / 30% testing and train a Random Forest (50 trees).
5. Report accuracy and a confusion matrix.
6. Run a simulated WIPS step: print an alert for each packet classified as an attack.

## Dataset
The CSV files come from the public AWID3 wireless dataset: https://www.kaggle.com/datasets/suumia/awid3-dataset?resource=download.

- `data/Deauth_0.csv` (normal traffic)
- `data/Deauth_1-selected-columns.csv` (attack traffic)

The combined dataset has 100,000 packets: 50,000 normal and 50,000 attack.

## Features
- `frame.len`
- `frame.time_delta`
- `frame.time_delta_displayed`

## Results
| Metric | Value |
|---|---|
| Accuracy | 67.56% |
| Test set size | 30,000 packets |

Confusion matrix (rows = actual, columns = predicted):

|  | Predicted normal | Predicted attack |
|---|---|---|
| **Actual normal** | 9,148 | 5,852 |
| **Actual attack** | 3,880 | 11,120 |

The model catches about 74% of attack packets but also flags about 39% of normal packets as attacks.

## Notes and limitations
- Earlier versions scored 99.99% to 100% using `frame.time_relative` and `frame.number`. These describe where a packet sits in its capture file, so the model could recognise the file instead of the attack. They were removed.
- Packet size and timing gaps are weak signals for a deauth flood. Better features would be the frame subtype, frames per second per device, and signal strength.
- The "block" action is simulated. It prints a message and does not block any device.

## Possible improvements
- Add the frame subtype and per-device frames per second as features.
- Split training and test data by time or by capture, instead of randomly.
- Use live capture in monitor mode on an authorised test network.
- Log alerts to a file and add a real response action.

## Run it
```bash
pip install -r requirements.txt
python WIDS.py
```

## Use of AI coding assistants
An AI coding assistant (Claude) was used to help write and adapt the code. AI coding assistants were utilized to structure the Scikit-learn data-loading pipeline and handle dataset merging. All feature selections, model evaluations, and script verifications were independently reviewed and tested.

## Ethics
The data comes from a public research dataset. Any traffic capture or attack generation must be done only on your own or an approved testbed.
