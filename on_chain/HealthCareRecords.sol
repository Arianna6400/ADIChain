// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// This contract is designed to manage health care records including medics, patients, caregivers,
// medical reports, and treatment plans efficiently and securely.
contract HealthCareRecords {
    // Structs for different entities within the health system, each with their specific attributes.
    struct Medic {
        string name;
        string lastname;
        string specialization;
        bool isRegistered;
        uint256 offChainId; // Identifier for references outside the blockchain
    }

    struct Patient {
        string name;
        string lastname;
        uint8 autonomous;
        bool isRegistered;
        uint256 offChainId; // Identifier for references outside the blockchain
        mapping(address => string) conditions; // Conditions updated by authorized medics
    }

    struct Caregiver {
        string name;
        string lastname;
        bool isRegistered;
    }

    struct Report {
        uint256 reportId; // Unique identifier for the report.
        uint256 patientId; // Link to the patient.
        uint256 medicId; // Link to the medic who created the report.
        string reportDetails; // Details of the medical report.
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
        uint actionId; // Unique identifier for each action taken within the system.
        string actionType; // Could be "Create", "Update", or "Delete".
        address initiatedBy; // Address of the user who initiated the action.
        uint256 timestamp; // Block timestamp when the action was logged.
        string details; // Additional details about the action
    }

    uint256 private actionCounter = 0; // Counter to keep track of actions for unique IDs.
    mapping(uint256 => Medic) public medics; // Mapping from ID to Medic struct.
    mapping(uint256 => Patient) public patients; // Mapping from ID to Patient struct.
    mapping(uint256 => Caregiver) public caregivers; // Mapping from ID to Caregiver struct.
    mapping(uint256 => Report) public reports; // Mapping from ID to Report struct.
    mapping(uint256 => TreatmentPlan) public treatmentPlans; // Mapping from ID to Treatment Plan struct.
    mapping(uint256 => ActionLog) public actionLogs; // Mapping from ID to ActionLog struct.
    mapping(address => bool) public authorizedEditors; // Mapping of addresses that are authorized to edit records.
    address public owner; // Address of the contract owner.

    // Constructor to initialize the owner and authorize them.
    constructor() {
        owner = msg.sender;
        authorizedEditors[owner] = true;
    }
    
    // Modifier to check if the caller is authorized to perform certain actions.
    modifier onlyAuthorized() {
        require(authorizedEditors[msg.sender], "Unauthorized access");// Check if the caller is authorized.
        _;
    }

    // Internal function to log any action taken within the contract.
    function logAction(string memory _actionType, address _initiator, string memory _details) internal {
        actionCounter++;
        actionLogs[actionCounter] = ActionLog(actionCounter, _actionType, _initiator, block.timestamp, _details);
    }

    // Public function to allow the owner to add an authorized editor.
    function addEditor(address _editor) public onlyAuthorized {
        authorizedEditors[_editor] = true;
    }

    // Public function to allow the owner to remove an authorized editor.
    function removeEditor(address _editor) public onlyAuthorized {
        authorizedEditors[_editor] = false;
    }

    // Function implementations for Medics, Patients, Caregivers, Reports, and Treatment Plans with a unique ID based on hashing of their details

    function addMedic(string memory name, string memory lastname, string memory specialization) public onlyAuthorized {
        uint256 offChainId = uint256(keccak256(abi.encodePacked(name, lastname, specialization)));
        require(medics[offChainId].offChainId == 0, "Medic already registered");
        medics[offChainId] = Medic(name, lastname, specialization, true, offChainId);
        logAction("Create", msg.sender, "Medic added");
    }

    function updateMedic(uint256 offChainId, string memory name, string memory lastname, string memory specialization, bool isRegistered) public onlyAuthorized {
        require(medics[offChainId].offChainId != 0, "Medic not found");
        Medic storage medic = medics[offChainId];
        medic.name = name;
        medic.lastname = lastname;
        medic.specialization = specialization;
        medic.isRegistered = isRegistered;
        logAction("Update", msg.sender, "Medic updated");
    }

    function addPatient(string memory name, string memory lastname, uint8 autonomous) public onlyAuthorized {
        uint256 offChainId = uint256(keccak256(abi.encodePacked(name, lastname)));
        require(patients[offChainId].offChainId == 0, "Patient already registered");
        
        Patient storage newPatient = patients[offChainId];
        newPatient.name = name;
        newPatient.lastname = lastname;
        newPatient.autonomous = autonomous;
        newPatient.isRegistered = true;
        newPatient.offChainId = offChainId;
        
        logAction("Create", msg.sender, "Patient added");
    }

    function updatePatient(uint256 offChainId, string memory name, string memory lastname, uint8 autonomous, bool isRegistered) public onlyAuthorized {
        require(patients[offChainId].offChainId != 0, "Patient not found");
        Patient storage patient = patients[offChainId];
        patient.name = name;
        patient.lastname = lastname;
        patient.autonomous = autonomous;
        patient.isRegistered = isRegistered;
        logAction("Update", msg.sender, "Patient updated");
    }

    function addCaregiver(string memory name, string memory lastname) public onlyAuthorized {
        uint256 id = uint256(keccak256(abi.encodePacked(name, lastname)));
        caregivers[id] = Caregiver(name, lastname, true);
        logAction("Create", msg.sender, "Caregiver added");
    }

    function updateCaregiver(uint256 id, bool newStatus) public onlyAuthorized {
        require(caregivers[id].isRegistered != newStatus, "No change in status");
        caregivers[id].isRegistered = newStatus;
        logAction("Update", msg.sender, "Caregiver status updated");
    }

    function addReport(uint256 patientId, uint256 medicId, string memory details) public onlyAuthorized {
        uint256 reportId = uint256(keccak256(abi.encodePacked(patientId, medicId, details)));
        reports[reportId] = Report(reportId, patientId, medicId, details);
        logAction("Create", msg.sender, "Report added");
    }

    function updateReport(uint256 reportId, string memory newDetails) public onlyAuthorized {
        require(keccak256(abi.encodePacked(reports[reportId].reportDetails)) != keccak256(abi.encodePacked(newDetails)), "No change in report details");
        reports[reportId].reportDetails = newDetails;
        logAction("Update", msg.sender, "Report updated");
    }

    function addTreatmentPlan(uint256 patientId, string memory details, string memory medication, uint256 startDate, uint256 endDate) public onlyAuthorized {
        uint256 planId = uint256(keccak256(abi.encodePacked(patientId, details, medication)));
        treatmentPlans[planId] = TreatmentPlan(planId, patientId, details, medication, startDate, endDate);
        logAction("Create", msg.sender, "Treatment plan added");
    }

    function updateTreatmentPlan(uint256 planId, string memory newDetails, string memory newMedication) public onlyAuthorized {
        require(keccak256(abi.encodePacked(treatmentPlans[planId].treatmentDetails)) != keccak256(abi.encodePacked(newDetails)), "No change in treatment details");
        treatmentPlans[planId].treatmentDetails = newDetails;
        treatmentPlans[planId].medication = newMedication;
        logAction("Update", msg.sender, "Treatment plan updated");
    }
}
