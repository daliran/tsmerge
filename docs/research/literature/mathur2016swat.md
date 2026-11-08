# mathur2016swat — SWaT: A Water Treatment Testbed for Research and Training on ICS Security

- **Status:** verified (2026-11-02): checked against the paper by an independent agent (about 115 claims: 3 misstatements, including one non-verbatim quote, and 1 unsourced detail, all fixed)
- **Reference:** Mathur, Tippenhauer; International Workshop on Cyber-physical Systems for Smart Water Networks (CySWater), 2016, pp. 31–36; DOI 10.1109/CySWater.2016.7469060 ([references.bib](references.bib); venue, pages and DOI come from Crossref, not from the PDF, which prints only "978-1-5090-1161-2/16/$31.00 ©2016 IEEE", p. 1)
- **Version read:** published version, 6 pages: main text pp. 1–6, references p. 6
- **Read:** everything (pp. 1–6), including Figures 1–3 (Figure 2 also at scale 3)
- **Code:** none given in the paper

## In one paragraph

The paper presents SWaT (Secure Water Treatment), an operational testbed for industrial control system (ICS) security research and training: a small-scale, six-stage water treatment plant, each stage controlled by its own PLCs, with sensors, actuators, a SCADA system, an HMI and a historian (p. 1, p. 2). It describes the physical process and the communication architecture (Section II, pp. 1–3), a first set of security experiments (attacker models, network reconnaissance, wireless and physical compromise, and two examples: sensor attacks on DPIT301 and LIT401, and invariant-based detection experiments) (Section III, pp. 3–5), a comparison with other testbeds (Section IV, p. 5) and lessons learned, including limits that make system identification and attack detection hard in some experiments (Section V, pp. 5–6). **It does not describe a released dataset:** there is no account of a recording campaign, its duration, normal and attack periods, labels or sampling rate.

## Problem

Academic ICS security research has little access to live ICS, where active security tests "are typically impossible"; as a result realistic examples of ICS are rare and theoretical assumptions "can be misleading" (p. 3). Many published attack and defense algorithms are assessed only through simulation or numerically (p. 1).

SWaT is in use to (a) understand the impact of cyber and physical attacks on a water treatment system, (b) assess attack detection algorithms, (c) assess defense mechanisms under attack, and (d) understand cascading effects of failures from one ICS to another dependent ICS (p. 1, abstract).

**Contributions as stated** (p. 1): (a) the design of a testbed for ICS cyber security research; (b) its use to assess methods for cyber attacks and defense against them.

## Method (the testbed)

### Physical plant

- An operational testbed "producing 5 US gallons/hr of filtered water", in about 90 square meters (p. 1; but see the throughput figures below).
- A small-scale version of a large modern water treatment plant (pp. 1–2); designed with Singapore's Public Utility Board and built by a third-party vendor, so that process and control "closely resemble real systems in the field" (p. 2).
- Raw water comes from the campus water line (drinkable) (p. 6); treated water is currently recycled within the process (p. 6), with permeate tank T501 returning water to T101 (Figure 2, p. 3).

**Throughput, as printed in three places** (they don't agree):

| Where | Value |
|---|---|
| p. 1 (Section II) | "5 US gallons/hr of filtered water" |
| p. 4 (Example 1) | "the nominal 5 gallons/minute" |
| p. 5 (Example 1 and Section IV) | "nearly 5 gallons/minute of treated water"; "a significant throughput of 5 US gallons per minute" |

### The six stages

From the text (p. 2) and Figure 2 (p. 3):

| Stage | Function (p. 2) | Components and tags in Figure 2 (p. 3) |
|---|---|---|
| P1 | Controls inflow of raw water by opening or closing a valve from the inlet pipe to the raw water tank | MV101 (valve), LIT101, raw water tank T101, pump P101 |
| P2 | Chemical dosing (chlorination) on the way to the UF feed tank | FIT201, AIT201; chemical tanks HCL, NaOCl, NaCl with dosing pumps P201, P203, P205; static mixer; AIT202, AIT203; MV201 |
| P3 | Ultrafiltration: a UF feed pump sends water through the UF membrane to the RO feed tank | LIT301, UF feed tank T301, UF feed pump P301, DPIT301, ultrafiltration unit (UF) |
| P4 | RO feed pump sends water through an ultraviolet dechlorinator (to remove free chlorine before RO); sodium bisulphate (NaHSO3) can be added to control ORP (Oxidation Reduction Potential) | LIT401, RO feed tank T401, RO feed pump P401, FIT401, UV dechlorinator, NaHSO3, AIT402 |
| P5 | De-chlorinated water passes a 3-stage RO filtration unit; permeate to the permeate tank, reject to the UF backwash tank | cartridge filter, AIT503, RO boost pump P501, reverse osmosis (RO) unit, AIT504 |
| P6 | Cleans the UF membranes by turning the UF backwash pump on or off | UF backwash tank T502, UF backwash pump P602, raw permeate tank T501, water return to T101 |

Tag abbreviations (Figure 2 caption, p. 3): LIT = Level Indicator and Transmitter; Pxxx = Pump; AITxxx = Property indicator and Transmitter; DPIT = Differential Pressure Indicator and Transmitter. FIT and MV aren't expanded in the caption; MV101 is "motorized valve 1 in process 1" (p. 2).

**UF backwash logic** (p. 2): started automatically "once every 30 minutes", taking "less than a minute"; also started if the pressure drop across the UF, measured by differential pressure sensors in P3 and read by PLC-3, "exceeds 0.4 bar".

**Sensor and actuator counts are not given:** the paper lists no total number of sensors or actuators, nor their types beyond the Figure 2 tags; it notes that actuators such as pumps "also have sensors to indicate their condition" (Figure 3 caption, p. 3).

### Control: PLCs

- Each stage is controlled by "its own set of dual PLCs", a primary and a backup (p. 2).
- Distributed control: each stage is controlled by its local PLCs; when a stage needs state from another, the PLCs exchange it over the network (p. 2). An operator can also control all actuators manually through the HMI and SCADA (p. 2).
- PLC model: "1756 ControlLogix", with SD card slots that could be used to update control logic (p. 4). HMI: "AB PanelView Plus Terminal" running embedded Windows, with an FTP server (anonymous login) and an RDP server (p. 4).
- **Tags** (p. 2): each PLC stores sensor data in memory locations called tags, one per connected sensor, accessible across all of SWaT (e.g. PLC 1 can read the level of T301 to decide whether to start P101). Tags are addressed by a designer-defined string (e.g. MV101) or by bank and pin number (p. 2).

### Network

| Layer | What it connects | Technology |
|---|---|---|
| Level 0 (L0) | each PLC with its own sensors and actuators | Ethernet ring, Allan-Bradley's Device Level Ring (DLR); tolerates the loss of a single link (p. 2; Figure 3, p. 3) |
| Level 1 (L1) | PLCs of the 6 stages with each other, plus HMI, SCADA and historian (p. 2) | Ethernet star with an industrial switch (p. 2) |
| Level 3 | SCADA and other computers (Figure 3 caption, p. 3) | not described; "not shown here" (p. 3). **Our reading:** this contradicts the text (p. 2) and Figure 3's own drawing, which put SCADA, the HMI and the historian on Level 1; the caption describes "a CPS" in general, not SWaT specifically |

- Protocols: EtherNet/IP (ENIP) and Common Industrial Protocol (CIP) for all communication by PLCs, sensors and actuators (p. 2); in the testbed ENIP has no authentication or encryption (p. 4).
- Wired or Wi-Fi links, switched by manual switches (p. 2). The wireless alternative to L1 uses MOXA AWK-5222-EU industrial access points with WPA2 and pre-shared keys (p. 4).

### Data collection

- "All sensor data, at every time instant, can be sent to the historian and saved for future analysis"; the historian is a separate computer on the Level 1 network (p. 2). Tag values are also sent to SCADA on demand (p. 2).
- Exporting historian data to CSV "currently requires manual intervention for each tag value", and getting the data out of the database exceeded the authors' expected effort (pp. 5–6).
- **No sampling rate is stated** for sensors, PLC scans or the historian.

## Experimental setup (attacks)

**Attacker models** (p. 3): A, with access to the local plant communication network; B, in physical proximity but not on site; C, on site with physical access to devices. In all cases the goal is to manipulate normal plant operation; an exemplary goal was overflowing the raw water tank (p. 3). For the first scenarios the attacker has general knowledge of the technology but not of the system's details (p. 3).

**Reconnaissance, attacker A** (pp. 3–4): a laptop on the L1 network with Wireshark and Zenmap mapped the network and services; web interfaces on PLCs and network devices; anonymous FTP on the HMI exposed hidden files with the HMI configuration; ARP spoofing with Ettercap (all PLCs, HMI and SCADA share one link-layer broadcast domain) allowed redirecting, eavesdropping and manipulating traffic; firmware and logic updates from SCADA to PLCs appear to travel in cleartext (p. 4).

**Wireless, attacker B** (p. 4): brute force on the pre-shared key or an evil-twin access point; the integrator's chosen password "would easily be guessable with a dictionary"; the AP's web interface, with its default password, exposed the Wi-Fi password in cleartext in the HTML source.

**Physical, attacker C** (p. 4): re-wiring cables, passive taps, manipulating sensors; the PLC SD card slot is a possible vector, "yet to be tested in practice".

**Conclusion on attackers** (p. 4): attackers A, B and C can fully manipulate L0 ring or L1 communication, act as man-in-the-middle and rewrite sensor or command values on the fly with Ettercap rules; the initial configuration had no means to detect or prevent the ARP spoofing attack.

## Results

**Example 1: attacks on sensor values** (pp. 4–5):

- Goal: degrade production below the nominal throughput (p. 4).
- **DPIT301 attack:** compromising the link from DPIT301 to PLC 3 and changing the value sent "from 20Kpa to 42kPa"; PLC 3 started a backwash because the pressure drop exceeded "the maximum acceptable, i.e., 40kpa" (p. 5). Earlier the threshold is printed as "higher than 0.40kpa" (p. 4) and as "0.4 bar" (p. 2).
- **LIT401 attack:** the level of the RO feed tank "as known to the PLC in stage 5" changed "from 800mm to 200mm", the PLC stopped pump P401, and production fell "to 113 gallons from the expected 155 gallons during the observation period" (p. 5). The RO output flow rate "must remain at about 1.2cm/hr which leads to nearly 5 gallons/minute" (p. 5). The length of the observation period is not given.

**Example 2: invariant-based detection** (p. 5): experiments on process-invariant (physics-based) detection gave design parameters for secure ICS: the number of data points the PLC logic uses to decide a control action, and the number the detector uses before announcing an attack; attack parameters such as the pulse width of intermittent attacks; and the finding that an attack on a sensor immediately before or after a power outage "is the most difficult to detect using invariant based approaches". No detection rates or other numbers are reported.

**What the paper does NOT state about a dataset** (checked on all 6 pages):

- No released dataset is described or announced.
- No recording duration, no split into normal and attack periods.
- No number of attacks in a recorded dataset (only the attack scenarios above, and the two process attacks of Example 1). The acknowledgements thank people for "collecting and sharing some of the data" and Section VI proposes making SWaT accessible online (p. 6), but neither describes a released dataset.
- No labeling scheme.
- No sampling rate.
- No total count of sensors, actuators or tags.
- No data format beyond the historian's manual CSV export (pp. 5–6).

## Assumptions and limitations

Stated by the authors:

- **Sensor availability** (p. 6): not all stages are adequately instrumented; e.g. there is no pH sensor at the UF output, so the UF's effect on pH can't be measured directly, which "might impact system identification studies where a linear dynamical model of only stages P1 through P3 is to be constructed". They recommend that it is "advisable to “over-instrument” the testbed" (p. 6), within physical, placement and cost limits.
- **Raw water** (p. 6): drinkable campus water, so attacks on water quality can't be studied with realistic impure input; the design is being modified to allow it.
- **Large tanks** (p. 5): the impact of an undetected attack takes significant time to show, compared with small tabletop testbeds.
- **Industrial software** (pp. 5–6): the SCADA and historian software is closed; data export is manual per tag.
- **Protocol choice** (p. 5): EtherNet/IP and CIP have little open-source tooling, unlike Modbus/TCP.
- **Preliminary results:** "the outlined experiments are just the first steps, and more detailed results will follow soon" (p. 3).
- The abstract says the experience "points to design limitations that make it difficult for system identification and attack detection in some experiments" (p. 1).

**Our reading:**

- The paper has internal inconsistencies in units: throughput is 5 gallons per hour (p. 1) or per minute (pp. 4–5); the UF threshold is 0.4 bar (p. 2), 0.40 kPa (p. 4) or 40 kPa (p. 5). 0.4 bar = 40 kPa, so p. 4's "0.40kpa" looks like a typo; the gallons/hr on p. 1 is probably also one, given two mentions of per minute. LIT401 belongs to stage P4 in Figure 2 but is read "by the PLC in stage 5" (p. 5).
- Figure 2's caption says "Dashed arrows indicate potential cyber attack points" (p. 3); in the figure the attack points seem to be the small "x" marks on the links, not dashed arrows.
- The paper says each stage has dual PLCs (p. 2), which implies 12 PLCs, but no number is printed; the abstract says each stage is controlled "by a local PLC" (p. 1).
- Section V-D is relevant to anomaly detection on SWaT: some physical effects aren't observable from the sensors.

## Relevance to this thesis

**Our reading:**

- **This is the testbed paper, not the dataset paper.** It supports the description of where SWaT data comes from (six stages, PLCs, L0/L1 networks, historian, tags such as LIT101, DPIT301, AIT201), but any fact about the SWaT dataset we use (duration, normal/attack split, number of attacks, labels, sampling rate, variable count) needs another source, and must not be cited to this paper.
- **Stage structure as a natural task split:** the six stages P1–P6 (p. 2, p. 3) with their own sensors and PLCs could define per-stage tasks or groups of channels; whether that's useful for joint training vs. merging is open.
- **Strong cross-stage couplings:** stages depend on each other's state (e.g. T301 level drives P101, p. 2), and attacks on one sensor show up in another stage's behavior (LIT401 → P401 → output volume, p. 5), so channels aren't independent.
- **Periodic normal behavior:** the UF backwash every 30 minutes (p. 2) is a regular pattern in normal operation that a forecaster or detector should learn, not flag.
- **Hard cases for detection:** attacks right before or after a power outage (p. 5), and quantities the sensors can't see (p. 6).

## Quotes worth keeping

> "SWaT consists of a 6-stage water treatment process, each stage is autonomously controlled by a local PLC." (p. 1)

> "Each stage is controlled by its own set of dual PLCs, one serving as a primary and the other as a backup in case of any failure of the primary." (p. 2)

> "All sensor data, at every time instant, can be sent to the historian and saved for future analysis." (p. 2)

> "The backwash cycle is initiated automatically once every 30 minutes and takes less than a minute to complete." (p. 2)

> "Perhaps the most interesting outcome of these experiments was the realization that an attack launched on a sensor immediately prior to power outage, or immediately following power outage, is the most difficult to detect using invariant based approaches." (p. 5)

> "While SWaT consist of a rich set of sensors, not all stages are equipped adequately." (p. 6)
