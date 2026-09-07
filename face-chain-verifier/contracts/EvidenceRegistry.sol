// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EvidenceRegistry {

    struct Evidence {
        string evidenceHash;
        string sourceUrl;
        uint256 timestamp;
        address submitter;
    }

    mapping(bytes32 => Evidence) private records;

    event EvidenceRegistered(
        bytes32 indexed recordId,
        string evidenceHash,
        string sourceUrl,
        uint256 timestamp,
        address submitter
    );

    function registerEvidence(
        string memory evidenceHash,
        string memory sourceUrl
    ) public returns (bytes32) {

        bytes32 recordId = keccak256(
            abi.encodePacked(
                evidenceHash,
                sourceUrl,
                block.timestamp,
                msg.sender
            )
        );

        records[recordId] = Evidence(
            evidenceHash,
            sourceUrl,
            block.timestamp,
            msg.sender
        );

        emit EvidenceRegistered(
            recordId,
            evidenceHash,
            sourceUrl,
            block.timestamp,
            msg.sender
        );

        return recordId;
    }

    function getEvidence(
        bytes32 recordId
    )
        public
        view
        returns (
            string memory,
            string memory,
            uint256,
            address
        )
    {
        Evidence memory evidence = records[recordId];

        return (
            evidence.evidenceHash,
            evidence.sourceUrl,
            evidence.timestamp,
            evidence.submitter
        );
    }
}