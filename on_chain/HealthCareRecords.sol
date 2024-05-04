// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HealthCareRecords {
    struct Medic {
        string name;
        string lastname;
        string specialization;
        bool isRegistered;
        uint256 offChainId;
    }

    struct Patient {
        string name;
        string lastname;
        uint8 autonomous;
        bool isRegistered;
        uint256 offChainId;
    }

    struct Caregiver {
        string name;
        string lastname;
        bool isRegistered;
        uint256 offChainId;
    }

    struct Report {
        uint256 reportId;
        uint256 patientId;
        uint256 medicId;
        string reportDetails;
    }

    struct TreatmentPlan {
        uint256 planId;
        uint256 patientId;
        string treatmentDetails;
        string medication;
        uint256 startDate;
        uint256 endDate;
    }

    struct ActionLog {
        uint256 actionId;
        string actionType;
        address initiatedBy;
        uint256 timestamp;
        string details;
    }

    uint256 private actionCounter = 0;
    mapping(uint256 => Medic) public medics;
    mapping(uint256 => Patient) public patients;
    mapping(uint256 => Caregiver) public caregivers;
    mapping(uint256 => Report) public reports;
    mapping(uint256 => TreatmentPlan) public treatmentPlans;
    mapping(uint256 => ActionLog) public actionLogs;
    mapping(address => bool) public authorizedEditors;
    address public owner;

    event ActionLogged(uint256 indexed actionId, string actionType, address indexed initiator, uint256 indexed timestamp, string details);

    constructor() {
        owner = msg.sender;
        authorizedEditors[owner] = true;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "This function is restricted to the contract owner.");
        _;
    }

    function generateOffChainId(string memory name, string memory lastname, string memory additionalData) private pure returns (uint256) {
        return uint256(keccak256(abi.encodePacked(name, lastname, additionalData)));
    }

    function authorizeEditor(address _editor) public onlyOwner {
        authorizedEditors[_editor] = true;
    }

    function revokeEditor(address _editor) public onlyOwner {
        authorizedEditors[_editor] = false;
    }

    function logAction(string memory _actionType, address _initiator, string memory _details) internal {
        actionCounter++;
        actionLogs[actionCounter] = ActionLog(actionCounter, _actionType, _initiator, block.timestamp, _details);
        emit ActionLogged(actionCounter, _actionType, _initiator, block.timestamp, _details);
    }

    function addMedic(string memory name, string memory lastname, string memory specialization) public onlyOwner {
        uint256 offChainId = generateOffChainId(name, lastname, specialization);
        require(medics[offChainId].isRegistered == false, "Medic already registered");
        medics[offChainId] = Medic(name, lastname, specialization, true, offChainId);
        logAction("Create", msg.sender, "Medic added");
    }

    function updateMedic(string memory name, string memory lastname, string memory specialization) public {
        uint256 offChainId = generateOffChainId(name, lastname, specialization);
        require(medics[offChainId].isRegistered == true, "Medic not found");
        Medic storage medic = medics[offChainId];
        medic.name = name;
        medic.lastname = lastname;
        medic.specialization = specialization;
        logAction("Update", msg.sender, "Medic updated");
    }

    function addPatient(string memory name, string memory lastname, uint8 autonomous) public onlyOwner {
        uint256 offChainId = generateOffChainId(name, lastname, "");
        require(patients[offChainId].isRegistered == false, "Patient already registered");
        Patient storage patient = patients[offChainId];
        patient.name = name;
        patient.lastname = lastname;
        patient.autonomous = autonomous;
        patient.isRegistered = true;
        patient.offChainId = offChainId;
        logAction("Create", msg.sender, "Patient added");
    }

    function updatePatient(string memory name, string memory lastname, uint8 autonomous) public {
        uint256 offChainId = generateOffChainId(name, lastname, "");
        require(patients[offChainId].isRegistered == true, "Patient not found");
        Patient storage patient = patients[offChainId];
        patient.name = name;
        patient.lastname = lastname;
        patient.autonomous = autonomous;
        logAction("Update", msg.sender, "Patient updated");
    }

    function addCaregiver(string memory name, string memory lastname) public onlyOwner {
        uint256 offChainId = generateOffChainId(name, lastname, "");
        require(caregivers[offChainId].isRegistered == false, "Caregiver already registered");
        caregivers[offChainId] = Caregiver(name, lastname, true, offChainId);
        logAction("Create", msg.sender, "Caregiver added");
    }

    function updateCaregiver(string memory name, string memory lastname) public {
        uint256 offChainId = generateOffChainId(name, lastname, "");
        require(caregivers[offChainId].isRegistered == true, "Caregiver not found");
        Caregiver storage caregiver = caregivers[offChainId];
        caregiver.name = name;
        caregiver.lastname = lastname;
        logAction("Update", msg.sender, "Caregiver status updated");
    }

    function addReport(uint256 patientId, uint256 medicId, string memory details) public onlyOwner {
        uint256 reportId = uint256(keccak256(abi.encodePacked(patientId, medicId, details)));
        reports[reportId] = Report(reportId, patientId, medicId, details);
        logAction("Create", msg.sender, "Report added");
    }

    function updateReport(uint256 reportId, string memory newDetails) public {
        require(keccak256(abi.encodePacked(reports[reportId].reportDetails)) != keccak256(abi.encodePacked(newDetails)), "No change in report details");
        reports[reportId].reportDetails = newDetails;
        logAction("Update", msg.sender, "Report updated");
    }

    function addTreatmentPlan(uint256 patientId, string memory details, string memory medication, uint256 startDate, uint256 endDate) public onlyOwner {
        uint256 planId = uint256(keccak256(abi.encodePacked(patientId, details, medication)));
        treatmentPlans[planId] = TreatmentPlan(planId, patientId, details, medication, startDate, endDate);
        logAction("Create", msg.sender, "Treatment plan added");
    }

    function updateTreatmentPlan(uint256 planId, string memory newDetails, string memory newMedication) public {
        require(keccak256(abi.encodePacked(treatmentPlans[planId].treatmentDetails)) != keccak256(abi.encodePacked(newDetails)), "No change in treatment details");
        treatmentPlans[planId].treatmentDetails = newDetails;
        treatmentPlans[planId].medication = newMedication;
        logAction("Update", msg.sender, "Treatment plan updated");
    }
}
