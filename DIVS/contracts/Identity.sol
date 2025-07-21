// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Identity {
    struct Credential {
        bytes32 hash; // Hash of user’s data (e.g., name + ID)
        address publicKey; // User’s Ethereum address
        bool isValid; // Credential status
    }

    mapping(address => Credential) public identities;

    event IdentityRegistered(address indexed user, bytes32 hash);
    event IdentityVerified(address indexed user, bool isValid);

    function registerIdentity(bytes32 _hash) public {
        require(identities[msg.sender].publicKey == address(0), "Identity already exists");
        identities[msg.sender] = Credential(_hash, msg.sender, true);
        emit IdentityRegistered(msg.sender, _hash);
    }

    function verifyIdentity(address _user, bytes32 _hash) public view returns (bool) {
        return identities[_user].isValid && identities[_user].hash == _hash;
    }

    function revokeIdentity() public {
        require(identities[msg.sender].publicKey != address(0), "Identity does not exist");
        identities[msg.sender].isValid = false;
        emit IdentityVerified(msg.sender, false);
    }
}