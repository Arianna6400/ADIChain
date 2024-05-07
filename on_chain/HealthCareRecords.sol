// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HealthCareRecords {
    struct Medic {
        string name;
        string lastname;
        string specialization;
        bool isRegistered;
    }

    struct Patient {
        string name;
        string lastname;
        uint8 autonomous;
        bool isRegistered;
    }

    struct Caregiver {
        string name;
        string lastname;
        bool isRegistered;
    }

    struct Report {
        uint256 reportId;
        address medicAddress;
        string analysis;
        string diagnosis;
    }

    struct TreatmentPlan {
        uint256 planId;
        address medicAddress;
        string treatmentDetails;
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
    mapping(address  => Medic) public medics;
    mapping(address  => Patient) public patients;
    mapping(address  => Caregiver) public caregivers;
    mapping(uint256 => Report) public reports;
    mapping(uint256 => TreatmentPlan) public treatmentPlans;
    mapping(uint256 => ActionLog) public actionLogs;
    mapping(address => bool) public authorizedEditors;
    address public owner;

    event EntityRegistered(string entityType, address indexed entityAddress);
    event EntityUpdated(string entityType, address indexed entityAddress);

    event ActionLogged(uint256 indexed actionId, string actionType, address indexed initiator, uint256 indexed timestamp, string details);

    constructor() {
        owner = msg.sender;
        authorizedEditors[owner] = true;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "This function is restricted to the contract owner.");
        _;
    }

    function authorizeEditor(address _editor) public onlyOwner {
        authorizedEditors[_editor] = true;
    }

    function logAction(string memory _actionType, address _initiator, string memory _details) internal {
        actionCounter++;
        actionLogs[actionCounter] = ActionLog(actionCounter, _actionType, _initiator, block.timestamp, _details);
        emit ActionLogged(actionCounter, _actionType, _initiator, block.timestamp, _details);
    }

    function addMedic(string memory name, string memory lastname, string memory specialization) public onlyOwner {
        require(!medics[msg.sender].isRegistered, "Medic already registered");
        medics[msg.sender] = Medic(name, lastname, specialization, true);
        logAction("Create", msg.sender, "Medic added");
        emit EntityRegistered("Medic", msg.sender);
    }

    function updateMedic(string memory name, string memory lastname, string memory specialization) public onlyOwner {
        require(medics[msg.sender].isRegistered, "Medic not found");
        Medic storage medic = medics[msg.sender];
        medic.name = name;
        medic.lastname = lastname;
        medic.specialization = specialization;
        logAction("Update", msg.sender, "Medic updated");
        emit EntityUpdated("Medic", msg.sender);
    }

    function addPatient(string memory name, string memory lastname, uint8 autonomous) public onlyOwner {
         require(!patients[msg.sender].isRegistered, "Patient already registered");
        Patient storage patient = patients[msg.sender];
        patient.name = name;
        patient.lastname = lastname;
        patient.autonomous = autonomous;
        patient.isRegistered = true;
        logAction("Create", msg.sender, "Patient added");
        emit EntityRegistered("Patient", msg.sender);
    }

    function updatePatient(string memory name, string memory lastname, uint8 autonomous) public onlyOwner {
        require(patients[msg.sender].isRegistered, "Patient not found");
        Patient storage patient = patients[msg.sender];
        patient.name = name;
        patient.lastname = lastname;
        patient.autonomous = autonomous;
        logAction("Update", msg.sender, "Patient updated");
        emit EntityUpdated("Patient", msg.sender);
    }

    function addCaregiver(string memory name, string memory lastname) public onlyOwner {
        require(caregivers[msg.sender].isRegistered == false, "Caregiver already registered");
        caregivers[msg.sender] = Caregiver(name, lastname, true);
        logAction("Create", msg.sender, "Caregiver added");
        emit EntityRegistered("Caregiver", msg.sender);
    }

    function updateCaregiver(string memory name, string memory lastname) public onlyOwner {
        require(caregivers[msg.sender].isRegistered, "Caregiver not found");
        Caregiver storage caregiver = caregivers[msg.sender];
        caregiver.name = name;
        caregiver.lastname = lastname;
        logAction("Update", msg.sender, "Caregiver status updated");
        emit EntityUpdated("Caregiver", msg.sender);
    }

    function addReport(address medicAddress, string memory analysis, string memory diagnosis) public onlyOwner {
        uint256 reportId = uint256(keccak256(abi.encodePacked(medicAddress, analysis, diagnosis, block.timestamp)));
        reports[reportId] = Report(reportId, medicAddress, analysis, diagnosis);
        logAction("Create", msg.sender, "Report added");
    }

    function addTreatmentPlan(address medicAddress, string memory details, uint256 startDate, uint256 endDate) public onlyOwner {
        uint256 planId = uint256(keccak256(abi.encodePacked(medicAddress, details, block.timestamp))); 
        treatmentPlans[planId] = TreatmentPlan(planId, medicAddress, details, startDate, endDate);
        logAction("Create", msg.sender, "Treatment plan added");
    }

    function updateTreatmentPlan(uint256 planId, string memory newDetails) public {
        require(msg.sender == owner || msg.sender == treatmentPlans[planId].medicAddress, "Unauthorized");
        require(keccak256(abi.encodePacked(treatmentPlans[planId].treatmentDetails)) != keccak256(abi.encodePacked(newDetails)), "No change in treatment details");
        treatmentPlans[planId].treatmentDetails = newDetails;
        logAction("Update", msg.sender, "Treatment plan updated");
    }
}
