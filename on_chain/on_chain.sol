// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Gestione di autorizzazioni basica con l'aggiunta di ruoli per medici e pazienti
contract MedicalDataSharing {
    
    address public admin; // L'indirizzo dell'amministratore del contratto

    // Struttura per i dati medici
    struct MedicalRecord {
        uint256 id;
        address patient; // Indirizzo Ethereum del paziente
        string dataHash; // Riferimento al dato medico salvato off-chain
        mapping(address => bool) accessPermission; // Mappatura di chi ha accesso al dato
    }

    // Mappatura degli ID dei record medici ai loro dati
    mapping(uint256 => MedicalRecord) public medicalRecords;

    // Mappatura degli indirizzi a ruoli, ad esempio medici, pazienti, ecc.
    mapping(address => bytes32) public roles;

    // Definizione degli eventi
    event RecordCreated(uint256 recordId);
    event AccessGranted(uint256 recordId, address indexed grantee);
    event AccessRevoked(uint256 recordId, address indexed grantee);

    // Modificatore che controlla se l'esecutore della funzione è l'amministratore del contratto
    modifier onlyAdmin {
        require(msg.sender == admin, "Unauthorized: Sender is not the admin");
        _;
    }

    // Modificatore che controlla se l'esecutore della funzione è il paziente associato al record medico
    modifier onlyPatient(uint256 _recordId) {
        require(msg.sender == medicalRecords[_recordId].patient, "Unauthorized: Sender is not the patient");
        _;
    }

    constructor() {
        admin = msg.sender; // Chi crea il contratto diventa l'amministratore
    }

    // Funzione per distruggere il contratto e inviare i fondi all'indirizzo dell'admin
    function destroyContract() external onlyAdmin {
        selfdestruct(payable(admin));
    }

    // Funzione per consentire all'amministratore di prelevare fondi
    function withdrawFunds() external onlyAdmin {
        payable(admin).transfer(address(this).balance);
    }

    // Funzione per assegnare un ruolo ad un indirizzo
    function assignRole(address _user, bytes32 _role) external onlyAdmin {
        roles[_user] = _role;
    }

    // Funzione per creare un nuovo record medico
    function createMedicalRecord(uint256 _id, address _patient, string memory _dataHash) public {
        require(roles[_patient] == keccak256("patient"), "Error: Address not registered as patient");
        require(medicalRecords[_id].patient == address(0), "Error: Record already exists");

        MedicalRecord storage record = medicalRecords[_id];
        record.id = _id;
        record.patient = _patient;
        record.dataHash = _dataHash;

        emit RecordCreated(_id);
    }

    // Funzione per consentire l'accesso al record medico
    function grantAccess(uint256 _recordId, address _grantee) public onlyPatient(_recordId) {
        medicalRecords[_recordId].accessPermission[_grantee] = true;
        emit AccessGranted(_recordId, _grantee);
    }

    // Funzione per revocare l'accesso al record medico
    function revokeAccess(uint256 _recordId, address _grantee) public onlyPatient(_recordId) {
        medicalRecords[_recordId].accessPermission[_grantee] = false;
        emit AccessRevoked(_recordId, _grantee);
    }

    // Funzione per controllare se un utente ha l'accesso a un record medico
    function hasAccess(uint256 _recordId, address _user) public view returns (bool) {
        return medicalRecords[_recordId].accessPermission[_user];
    }

    // Altre funzioni possono includere l'aggiornamento dei dati medici, il loro recupero, ecc.
    // ...
}

// #GiaccoGay
// #coglione