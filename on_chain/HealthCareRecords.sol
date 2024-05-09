// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

//Documentation for this contract written in NatSpec format
/**
 * @title Health Care Records System
 * @dev Manages healthcare records for patients, medics, and caregivers.
 * @notice This contract is intended for demonstration purposes and not for production use.
 */
contract HealthCareRecords {
    // Structs for every type of user
    struct Medic {
        string name;
        string lastName;
        string specialization;
        bool isRegistered;
    }

    struct Patient {
        string name;
        string lastName;
        uint8 autonomous;
        bool isRegistered;
    }

    struct Caregiver {
        string name;
        string lastName;
        bool isRegistered;
    }

    // Struct for medical report
    struct Report {
        uint256 reportId;
        address medicAddress;
        string analysis;
        string diagnosis;
    }

    //Struct for medical treatment plan
    struct TreatmentPlan {
        uint256 planId;
        address medicAddress;
        string treatmentDetails;
        string startDate;
        string endDate;
    }

    //Struct to log actions for every previous struct
    struct ActionLog {
        uint256 actionId;
        string actionType;
        address initiatedBy;
        uint256 timestamp;
        string details;
    }

    //State variables and mapping
    uint256 private actionCounter = 0;
    mapping(address  => Medic) public medics;
    mapping(address  => Patient) public patients;
    mapping(address  => Caregiver) public caregivers;
    mapping(uint256 => Report) public reports;
    mapping(uint256 => TreatmentPlan) public treatmentPlans;
    mapping(uint256 => ActionLog) public actionLogs;
    mapping(address => bool) public authorizedEditors;
    address public owner;

    //Events for actions
    event EntityRegistered(string entityType, address indexed entityAddress);
    event EntityUpdated(string entityType, address indexed entityAddress);
    event ActionLogged(uint256 indexed actionId, string actionType, address indexed initiator, uint256 indexed timestamp, string details);

    /**
     * @dev Sets the contract owner as the deployer and initializes authorized editors.
     */
    constructor() {
        owner = msg.sender;
        authorizedEditors[owner] = true;
    }

    //Modifiers
    /**
     * @dev Restricts function access to the contract owner only.
     */
    modifier onlyOwner() {
        require(msg.sender == owner, "This function is restricted to the contract owner.");
        _;
    }

    /**
     * @dev Restricts function access to either the contract owner or authorized editors.
     */
    modifier onlyAuthorized() {
        require(msg.sender == owner || authorizedEditors[msg.sender], "Access denied: caller is not the owner or an authorized editor.");
        _;
    }

    // Functions
    /**
     * @dev Authorizes a new editor to manage records.
     * @param _editor Address of the new editor to authorize.
     */
    function authorizeEditor(address _editor) public onlyOwner {
        authorizedEditors[_editor] = true;
    }

    /**
     * @dev Logs actions taken by users within the system for auditing purposes.
     * @param _actionType Type of action performed.
     * @param _initiator Address of the user who initiated the action.
     * @param _details Details or description of the action.
     */
    function logAction(string memory _actionType, address _initiator, string memory _details) internal {
        actionCounter++;
        actionLogs[actionCounter] = ActionLog(actionCounter, _actionType, _initiator, block.timestamp, _details);
        emit ActionLogged(actionCounter, _actionType, _initiator, block.timestamp, _details);
    }

    /**
     * @dev Adds a new medic record to the system.
     * @param name First name of the medic.
     * @param lastname Last name of the medic.
     * @param specialization Medical specialization of the medic.
     * @notice Only authorized users can add medic records.
     */
    function addMedic(string memory name, string memory lastname, string memory specialization) public onlyAuthorized {
        require(!medics[msg.sender].isRegistered, "Medic already registered");
        medics[msg.sender] = Medic(name, lastname, specialization, true);
        logAction("Create", msg.sender, "Medic added");
        emit EntityRegistered("Medic", msg.sender);
    }

    /**
     * @dev Updates existing medic information.
     * @param name Updated first name of the medic.
     * @param lastname Updated last name of the medic.
     * @param specialization Updated medical specialization of the medic.
     * @notice Only authorized users can update medic records.
     */
    function updateMedic(string memory name, string memory lastname, string memory specialization) public onlyAuthorized {
        require(medics[msg.sender].isRegistered, "Medic not found");
        Medic storage medic = medics[msg.sender];
        medic.name = name;
        medic.lastName = lastname;
        medic.specialization = specialization;
        logAction("Update", msg.sender, "Medic updated");
        emit EntityUpdated("Medic", msg.sender);
    }

    /**
     * @dev Adds a new patient record to the system.
     * @param name First name of the patient.
     * @param lastname Last name of the patient.
     * @param autonomous Level of autonomy of the patient.
     * @notice Only authorized users can add patient records.
     */
    function addPatient(string memory name, string memory lastname, uint8 autonomous) public onlyAuthorized {
         require(!patients[msg.sender].isRegistered, "Patient already registered");
        Patient storage patient = patients[msg.sender];
        patient.name = name;
        patient.lastName = lastname;
        patient.autonomous = autonomous;
        patient.isRegistered = true;
        logAction("Create", msg.sender, "Patient added");
        emit EntityRegistered("Patient", msg.sender);
    }

    /**
     * @dev Updates existing patient information.
     * @param name Updated first name of the patient.
     * @param lastname Updated last name of the patient.
     * @param autonomous Updated level of autonomy of the patient.
     * @notice Only authorized users can update patient records.
     */
    function updatePatient(string memory name, string memory lastname, uint8 autonomous) public onlyAuthorized {
        require(patients[msg.sender].isRegistered, "Patient not found");
        Patient storage patient = patients[msg.sender];
        patient.name = name;
        patient.lastName = lastname;
        patient.autonomous = autonomous;
        logAction("Update", msg.sender, "Patient updated");
        emit EntityUpdated("Patient", msg.sender);
    }

    /**
     * @dev Adds a new caregiver record to the system.
     * @param name First name of the caregiver.
     * @param lastname Last name of the caregiver.
     * @notice Only authorized users can add caregiver records.
     */
    function addCaregiver(string memory name, string memory lastname) public onlyAuthorized {
        require(caregivers[msg.sender].isRegistered == false, "Caregiver already registered");
        caregivers[msg.sender] = Caregiver(name, lastname, true);
        logAction("Create", msg.sender, "Caregiver added");
        emit EntityRegistered("Caregiver", msg.sender);
    }

     /**
     * @dev Updates existing caregiver information.
     * @param name Updated first name of the caregiver.
     * @param lastname Updated last name of the caregiver.
     * @notice Only authorized users can update caregiver records.
     */
    function updateCaregiver(string memory name, string memory lastname) public onlyAuthorized {
        require(caregivers[msg.sender].isRegistered, "Caregiver not found");
        Caregiver storage caregiver = caregivers[msg.sender];
        caregiver.name = name;
        caregiver.lastName = lastname;
        logAction("Update", msg.sender, "Caregiver status updated");
        emit EntityUpdated("Caregiver", msg.sender);
    }

    /**
     * @dev Adds a new medical report to the system.
     * @param analysis Medical analysis details.
     * @param diagnosis Medical diagnosis.
     * @notice Only authorized users can add medical reports.
     */
    function addReport(string memory analysis, string memory diagnosis) public onlyAuthorized {
        uint256 reportId = uint256(keccak256(abi.encodePacked(msg.sender, analysis, diagnosis, block.timestamp)));
        reports[reportId] = Report(reportId, msg.sender, analysis, diagnosis);
        logAction("Create", msg.sender, "Report added");
    }

    /**
     * @dev Adds a new treatment plan to the system.
     * @param treatmentDetails Treatment details.
     * @param startDate Start date of the treatment.
     * @param endDate End date of the treatment.
     * @notice Only authorized users can add treatment plans.
     */
    function addTreatmentPlan(string memory treatmentDetails, string memory startDate, string memory endDate) public onlyAuthorized {
        uint256 planId = uint256(keccak256(abi.encodePacked(msg.sender, treatmentDetails, block.timestamp))); 
        treatmentPlans[planId] = TreatmentPlan(planId, msg.sender, treatmentDetails, startDate, endDate);
        logAction("Create", msg.sender, "Treatment plan added");
    }

    /**
     * @dev Updates an existing treatment plan with new details, start date, and end date.
     * @param planId Identifier of the treatment plan to update.
     * @param treatmetDetails New details of the treatment plan.
     * @param startDate New start date of the treatment.
     * @param endDate New end date of the treatment.
     * @notice Requires the caller to be either the owner or the medic associated with the treatment plan.
     * @notice Assumes the treatment plan exists and the caller has proper authorization.
     */    
    function updateTreatmentPlan(uint256 planId, string memory treatmetDetails, string memory startDate, string memory endDate) public onlyAuthorized {
        require(msg.sender == owner || msg.sender == treatmentPlans[planId].medicAddress, "Unauthorized");
        treatmentPlans[planId].treatmentDetails = treatmetDetails;
        treatmentPlans[planId].startDate = startDate;
        treatmentPlans[planId].endDate = endDate;
        logAction("Update", msg.sender, "Treatment plan updated");
    }
}
