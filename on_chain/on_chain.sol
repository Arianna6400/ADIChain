// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// This contract manages health care records within a decentralized platform.
contract HealthCareRecords {
    // Structure to hold medic details
    struct Medic {
        string name;
        string lastname;
        string specialization;
        bool isRegistered; // flag to check registration status
        uint256 offChainId; // identifier for off-chain database
    }
    
    // Structure to hold patient details
    struct Patient {
        string name;
        string lastname;
        bool isRegistered; // flag to check registration status
        bool autonomous; // flag for patient autonomy
        uint256 offChainId; // identifier for off-chain database
        mapping(address => address) authorizedMedics; // mapping to track authorized medics
        mapping(address => uint256) patientTreatmentPlan; // mapping to track treatment plans
        mapping(address => uint256) reportResult; // mapping to track diagnostic reports
    }

    // Structure for caregivers
    struct Caregivers {
        string name;
        string lastname;
        bool isRegistered; // flag to check registration status
        uint256 offChainId; // identifier for off-chain database
        mapping(address => address) caredPatient; // mapping to track patients under care
    }

    // Structure to hold login credentials
    struct Credentials {
        uint256 offChainId; // identifier for off-chain database
        string username;
        string hash_password;
        string role;
        string public_key;
        string private_key;
    }

    // Structure to hold reports
    struct Reports {
        uint256 offChainId; // identifier for off-chain database
        string analysis;
        string diagnosis;
        uint256 medic_id; // identifier for the medic who created the report
    }

    // Structure to hold treatment plans
    struct TreatmentPlan {
        uint256 offChainId; // identifier for off-chain database
        string medic_id;
        string caregiver_id;
        string description;
        string start_date;
        string end_date;
    }

    // Mappings to ensure uniqueness of reports and treatment plans
    mapping(bytes32 => bool) private reportHashes;
    mapping(bytes32 => bool) private treatmentPlanHashes;

    // Public mappings to access medic and patient details
    mapping(address => Medic) public medics;
    mapping(address => Patient) public patients;

    // Events to signal actions within the contract
    event MedicRegistered(address indexed medicAddress, string name, string specialization, uint256 offChainId);
    event PatientRegistered(address indexed patientAddress, string name, uint256 offChainId);
    event AccessGranted(address indexed patientAddress, address indexed medicAddress);
    event ReportHashLogged(bytes32 reportHash);
    event TreatmentPlanHashLogged(bytes32 treatmentPlanHash);

    // Modifiers to restrict function calls to registered users
    modifier onlyRegisteredMedic {
        require(medics[msg.sender].isRegistered, "Medic not registered.");
        _;
    }

    modifier onlyRegisteredPatient {
        require(patients[msg.sender].isRegistered, "Patient not registered.");
        _;
    }

    // Function to register a medic
    function registerMedic(string memory name, string memory lastname, string memory specialization, uint256 offChainId) public {
        require(!medics[msg.sender].isRegistered, "Medic already registered.");
        require(bytes(name).length > 0 && bytes(lastname).length > 0 && bytes(specialization).length > 0, "Invalid input data");
        medics[msg.sender] = Medic(name, lastname, specialization, true, offChainId);
        emit MedicRegistered(msg.sender, name, specialization, offChainId);
    }

    // Function to register a patient
    function registerPatient(string memory name, uint256 offChainId) public {
        require(!patients[msg.sender].isRegistered, "Patient already registered.");
        require(bytes(name).length > 0, "Invalid name input");
        Patient storage patient = patients[msg.sender];
        patient.name = name;
        patient.isRegistered = true;
        patient.offChainId = offChainId;

        emit PatientRegistered(msg.sender, name, offChainId);
    }

    // Function to grant a medic access to a patient's records
    function grantAccessToMedic(address medicAddress) public onlyRegisteredPatient {
        require(medics[medicAddress].isRegistered, "Medic not registered.");
        patients[msg.sender].authorizedMedics[medicAddress] = medicAddress;
        emit AccessGranted(msg.sender, medicAddress);
    }

    // Function to log report hashes, ensuring reports are unique and tracked
    function logReportHash(bytes32 reportHash) public onlyRegisteredMedic {
        reportHashes[reportHash] = true;
        emit ReportHashLogged(reportHash);
    }

    // Function to log treatment plan hashes, ensuring treatment plans are unique and tracked
    function logTreatmentPlanHash(bytes32 treatmentPlanHash) public onlyRegisteredMedic {
        treatmentPlanHashes[treatmentPlanHash] = true;
        emit TreatmentPlanHashLogged(treatmentPlanHash);
    }

    // View function to check if a report hash is logged
    function isReportHashLogged(bytes32 reportHash) public view returns (bool) {
        return reportHashes[reportHash];
    }

    // View function to check if a treatment plan hash is logged
    function isTreatmentPlanHashLogged(bytes32 treatmentPlanHash) public view returns (bool) {
        return treatmentPlanHashes[treatmentPlanHash];
    }
}
