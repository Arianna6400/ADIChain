// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// This contract is designed to manage health care records efficiently and securely. 
// It includes functionality for registering and managing medics, patients, caregivers, medical reports, and treatment plans.
contract HealthCareRecords {
    // Defines a Medic with various attributes including registration status and an identifier for off-chain references.
    struct Medic {
        string name;
        string lastname;
        string specialization;
        bool isRegistered;
        uint256 offChainId; // using uint32 instead of uint256 to save gas (although this comment should match the actual type used)
    }
    
    // Defines a Patient, including a mapping to store conditions updated by authorized medics.
    struct Patient {
        string name;
        string lastname;
        bool autonomous; // Indicates if the patient can manage their own records
        bool isRegistered;
        uint256 offChainId;
        mapping(address => string) authorizedMedics; // Maps medic addresses to the patient's condition as updated by them
    }
    
    // Defines a Caregiver with registration status.
    struct Caregiver {
        string name;
        string lastname;
        bool isRegistered;
    }
    
    // Defines a Report containing detailed medical reports written by medics.
    struct Report {
        uint256 reportId;
        uint256 patientId;
        uint256 medicId;
        string reportDetails;
    }
    
    // Defines a Treatment Plan outlining the treatment details and medication for a patient.
    struct TreatmentPlan {
        uint256 planId;
        uint256 patientId;
        string treatmentDetails;
        string medication;
        uint256 startDate;
        uint256 endDate;
    }

    // Mappings to store Medics, Patients, Caregivers, Reports, and Treatment Plans.
    mapping(uint256 => Medic) public medics;
    mapping(uint256 => Patient) public patients;
    mapping(uint256 => Caregiver) public caregivers;
    mapping(uint256 => Report) public reports;
    mapping(uint256 => TreatmentPlan) public treatmentPlans;

    // Events that notify watchers of changes to the contract state.
    event MedicRegistered(uint256 indexed medicId, string name);
    event PatientRegistered(uint256 indexed patientId, string name);
    event CaregiverRegistered(uint256 indexed caregiverId, string name);
    event ReportFiled(uint256 indexed reportId, uint256 patientId, uint256 medicId);
    event TreatmentPlanCreated(uint256 indexed planId, uint256 patientId, string treatmentDetails);

    bool public paused = false; // Flag to manage contract pausability.
    address public owner; // Address of the contract's owner.

    // Modifier to restrict functions to the owner.
    modifier onlyOwner() {
        require(msg.sender == owner, "Not the owner");
        _;
    }

    // Modifier to ensure functions are callable only when the contract is not paused.
    modifier whenNotPaused() {
        require(!paused, "Contract is paused");
        _;
    }

    // Contract constructor that sets the owner upon deployment.
    constructor() {
        owner = msg.sender;
    }

    // Allows the owner to pause the contract.
    function pause() public onlyOwner {
        paused = true;
    }

    // Allows the owner to unpause the contract.
    function unpause() public onlyOwner {
        paused = false;
    }

    // Modifier to check that a medic is registered before they perform certain actions.
    modifier onlyRegisteredMedic(uint256 _medicId) {
        require(medics[_medicId].isRegistered, "Only registered medics can perform this action");
        _;
    }

    // Registers a medic, emitting an event upon success.
    function registerMedic(uint256 _id, string memory _name, string memory _lastname, string memory _specialization) public onlyOwner whenNotPaused {
        require(!medics[_id].isRegistered, "Medic is already registered");
        medics[_id] = Medic(_name, _lastname, _specialization, true, _id);
        emit MedicRegistered(_id, _name);
    }

    // Registers a patient, emitting an event upon success.
    function registerPatient(uint256 _id, string memory _name, string memory _lastname, bool _autonomous) public onlyOwner whenNotPaused {
        require(!patients[_id].isRegistered, "Patient is already registered");
        Patient storage patient = patients[_id];
        patient.name = _name;
        patient.lastname = _lastname;
        patient.autonomous = _autonomous;
        patient.isRegistered = true;
        patient.offChainId = _id;
        emit PatientRegistered(_id, _name);
    }

    // Registers a caregiver.
    function registerCaregiver(uint256 _id, string memory _name, string memory _lastname) public onlyOwner whenNotPaused {
        caregivers[_id] = Caregiver(_name, _lastname, true);
    }

    // Updates the condition of a patient, allowing updates by authorized medics only.
    function updatePatient(uint256 _id, string memory _condition) public whenNotPaused {
        require(patients[_id].offChainId != 0, "Patient not found");
        patients[_id].authorizedMedics[msg.sender] = _condition;
    }

    // Files a medical report, restricted to registered medics.
    function fileReport(uint256 _reportId, uint256 _patientId, uint256 _medicId, string memory _details) public onlyRegisteredMedic(_medicId) whenNotPaused {
        require(medics[_medicId].isRegistered, "Medic not registered");
        reports[_reportId] = Report(_reportId, _patientId, _medicId, _details);
    }

    // Creates a treatment plan, restricted to registered medics.
    function createTreatmentPlan(uint256 _planId, uint256 _patientId, uint256 _medicId, string memory _treatmentDetails, string memory _medication, uint256 _startDate, uint256 _endDate) public onlyRegisteredMedic(_medicId) whenNotPaused {
        treatmentPlans[_planId] = TreatmentPlan(_planId, _patientId, _treatmentDetails, _medication, _startDate, _endDate);
    }
}
