# Decentralized private set membership protocol for private location in sharing economy

_Submission in progress._

This repository provides the source code used to evaluate the APSI protocol proposed in the article _Decentralized 
private set membership protocol for private location in sharing economy_.

## Abstract

<img src="/graphical_abstract.png?raw=true" alt="drawing" width="500"/>

In this article, we focus on personal data management in service exchange networks, where members meet each other to 
share services based on their skill. Through the case study of the Accorderie (a Quebec solidarity cooperative), we 
propose an innovative protocol designed to reinforce the confidentiality of data relative to members' addresses and 
service intervention locations. Using distributed ledger and peer-to-peer interaction, our proposition minimizes the 
Accorderie's direct involvement while keeping its position as a trusted authority, allowing members to engage in direct 
interactions without reliance on a centralized platform. We present three versions of private set membership protocols 
specially designed to manage locations in sharing economy. Finally, our findings suggest that decentralized solutions 
could be a relevant support for solidarity communities, in particular by enhancing member privacy and security, but 
also by facilitating and reducing maintenance costs.

## Usage
- `schnorr.py` can be used (as main) to build a schnorr group accordingly to
[Schnorr group](https://en.wikipedia.org/wiki/Schnorr_group). 
The generated group is pickled in a gitignored file `schnorr_group_[id].data`.
- `protocol_v1.py` (v2 and v3) can be used (as main) to measure execution times.
- Results must be manually report in `plotter.py` to build `times_plot.png`.

## Results
The current version of the article will be available soon.

[//]: # (The provided PDF is the current version of the article and results can be found in the evaluation section.)

The measured times included in this code (accessible in `potter.py`), and corresponding to the figure of the 
article, were measured in July 2025 on an Intel Core Ultra 268V processor.
